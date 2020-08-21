provider "aws" {
  region  = "${var.aws_region}"
}

terraform {
  backend "s3" {
    region = "us-east-1"
  }
}