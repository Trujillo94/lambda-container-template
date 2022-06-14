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

variable "AWS_ACCESS_KEY_ID" {
  type     = string
  nullable = false
}

variable "AWS_SECRET_ACCESS_KEY" {
  type      = string
  sensitive = true
  nullable  = false
}

variable "REPOSITORY_NAME" {
  type      = string
  sensitive = false
  nullable  = false
}

variable "AWS_ECR_REPO" {
  type      = string
  sensitive = false
  nullable  = true
}

provider "aws" {
  region     = var.region
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

data "aws_caller_identity" "current" {}

locals {
  project_name        = var.REPOSITORY_NAME
  account_id          = data.aws_caller_identity.current.account_id
  ecr_repository_name = var.AWS_ECR_REPO || local.project_name
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

resource "aws_api_gateway_rest_api" "template_api" {
  name        = "template-api"
  description = "This is my API for demonstration purposes"
}

resource "aws_api_gateway_resource" "MyDemoResource" {
  rest_api_id = aws_api_gateway_rest_api.template_api.id
  parent_id   = aws_api_gateway_rest_api.template_api.root_resource_id
  path_part   = "mydemoresource"
}

resource "aws_api_gateway_method" "demo_method" {
  rest_api_id   = aws_api_gateway_rest_api.template_api.id
  resource_id   = aws_api_gateway_resource.MyDemoResource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "MyDemoIntegration" {
  rest_api_id          = aws_api_gateway_rest_api.template_api.id
  resource_id          = aws_api_gateway_resource.MyDemoResource.id
  http_method          = aws_api_gateway_method.demo_method.http_method
  type                 = "AWS"
  uri                  = aws_lambda_function.lambda_function.invoke_arn
  timeout_milliseconds = 29000

  request_parameters = {
    "integration.request.header.X-Authorization" = "'static'"
  }



  # Transforms the incoming XML request to JSON
  request_templates = {
    "application/xml" = <<EOF
{
  "body" : $input.json('$')
}
EOF
  }
}
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${var.myregion}:${var.access_key}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method.http_method}${aws_api_gateway_resource.resource.path}"
}
output "lambda_name" {
  value = aws_lambda_function.lambda_function.id
}


