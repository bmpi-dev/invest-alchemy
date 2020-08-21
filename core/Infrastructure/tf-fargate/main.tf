provider "aws" {
  region  = "${var.aws_region}"
}

terraform {
  backend "s3" {
    region = "eu-west-1"
  }
}