terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}
variable "region" {
  default = "eu-west-3"
}



provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

locals {
  project_name        = "lambda-container-template-terraform"
  account_id          = data.aws_caller_identity.current.account_id
  ecr_repository_name = local.project_name
  ecr_image_tag       = "latest"
}

resource "aws_ecr_repository" "repo" {
  name = local.ecr_repository_name
}

resource "null_resource" "ecr_image" {
  triggers = {
    python_file = md5(file("${path.module}/main.py"))
    docker_file = md5(file("${path.module}/Dockerfile"))
  }

  provisioner "local-exec" {
    command = <<EOF
           aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com
           cd ${path.module}/
           docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} .
           docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
       EOF
  }
}

data "aws_ecr_image" "lambda_image" {
  depends_on = [
    null_resource.ecr_image
  ]
  repository_name = local.ecr_repository_name
  image_tag       = local.ecr_image_tag
}

resource "aws_iam_role" "lambda" {
  name               = "${local.project_name}-lambda-role"
  assume_role_policy = <<EOF
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Action": "sts:AssumeRole",
           "Principal": {
               "Service": "lambda.amazonaws.com"
           },
           "Effect": "Allow"
       }
   ]
}
 EOF
}

data "aws_iam_policy_document" "lambda" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect    = "Allow"
    resources = ["*"]
    sid       = "CreateCloudWatchLogs"
  }

  statement {
    actions = [
      "codecommit:GitPull",
      "codecommit:GitPush",
      "codecommit:GitBranch",
      "codecommit:ListBranches",
      "codecommit:CreateCommit",
      "codecommit:GetCommit",
      "codecommit:GetCommitHistory",
      "codecommit:GetDifferences",
      "codecommit:GetReferences",
      "codecommit:BatchGetCommits",
      "codecommit:GetTree",
      "codecommit:GetObjectIdentifier",
      "codecommit:GetMergeCommit"
    ]
    effect    = "Allow"
    resources = ["*"]
    sid       = "CodeCommit"
  }
}

resource "aws_iam_policy" "lambda" {
  name   = "${local.project_name}-lambda-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.lambda.json
}

resource "aws_lambda_function" "lambda_function" {
  depends_on = [
    null_resource.ecr_image
  ]
  function_name = local.project_name
  role          = aws_iam_role.lambda.arn
  timeout       = 30
  image_uri     = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.lambda_image.id}"
  package_type  = "Image"
}

output "lambda_name" {
  value = aws_lambda_function.lambda_function.id
}


