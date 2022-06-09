terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.2.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3"
}

resource "aws_budgets_budget" "budget-limit" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "25.00"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2022-09-06_00:01"
}

module "lambda_example_container-image" {
  source  = "terraform-aws-modules/lambda/aws//examples/container-image"
  version = "3.2.1"
}
