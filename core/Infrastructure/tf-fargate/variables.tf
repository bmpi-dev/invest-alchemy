variable "aws_region" {
  default = "us-east-1"
  description = "AWS Region"
}

variable "env" {
  default     = "dev"
  description = "Environment"
}

variable "project" {
  default     = "invest-alchemy-core"
  description = "Project Name"
}

variable "description" {
  default     = "invest alchemy core service"
  description = "Project Description"
}

variable "artifacts_bucket" {
  default     = "invest-alchemy"
  description = "Artifacts Bucket Name"
}

variable "ecs_event_role" {
  default     = "XXX"
  description = "IAM Role used for CloudWatch"
}

variable "ecs_taskexec_role" {
  default     = "XXX"
  description = "IAM Role used for Task Execution"
}

variable "subnets_ids" {
  type        = list(string)
  default     = ["XXX"]
  description = "Subnets IDs used for Fargate Containers"
}

variable "security_groups_ids" {
  type        = list(string)
  default     = ["sg-0f1fe5a3bcc61f5ce"]
  description = "Security Groups IDs used for Fargate"
}

variable "schedule" {
  default     = "cron(0 0 ? * MON-FRI *)"
  description = "Schedule for your job"
}

variable "assign_public_ip" {
  default     = "true"
  description = "Set public IP on Fargate Container"
}

variable "ecs_cpu_units" {
  default     = "256"
  description = "Container: Number of CPU Units"
}

variable "ecs_memory" {
  default     = "512"
  description = "Container: Memory in MB"
}

variable "ecr_image_uri" {
  default     = "745121664662.dkr.ecr.us-east-1.amazonaws.com/invest-alchemy-core-ecr-dev:latest"
  description = "URI of the Docker Image in ECR"
}

variable "TUSHARE_API_TOKEN" {
  description = "Tushare API Token from .env"
  type        = string
}

variable "TG_BOT_API_TOKEN" {
  description = "TG API Token from .env"
  type        = string
}

variable "TG_CHAT_IDS" {
  description = "TG API Chat Ids from .env"
  type        = string
}

variable "PG_DB_URL" {
  description = "Main Database Connection URL"
  type        = string
}

variable "PG_DB_PWD" {
  description = "Main Database Password"
  type        = string
}

variable "APP_ENV" {
  description = "App Environment"
  type        = string
}

variable "SMTP_ADDRESS" {
  description = "SMTP address"
  type        = string
}

variable "SMTP_PORT" {
  description = "SMTP port"
  type        = string
}

variable "SMTP_USERNAME" {
  description = "SMTP username"
  type        = string
}

variable "SMTP_PASSWORD" {
  description = "SMTP password"
  type        = string
}

variable "SMTP_MAIL_FROM" {
  description = "SMTP mail from"
  type        = string
}

variable "SMTP_MAIL_FROM_ALIAS" {
  description = "SMTP mail from alias"
  type        = string
}