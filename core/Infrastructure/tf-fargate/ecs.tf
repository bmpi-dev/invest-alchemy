
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project}_ecs_cluster_${var.env}"

  tags = {
    Project     = "${var.project}"
    Environment = "${var.env}"
  }
}

resource "aws_ecs_cluster_capacity_providers" "ecs_cluster_capacity_provider" {
  cluster_name = aws_ecs_cluster.ecs_cluster.name

  capacity_providers = ["FARGATE_SPOT"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = "100"
  }
}

resource "aws_ecs_task_definition" "task_definition" {
  family                   = "${var.project}_task_definition_${var.env}"
  container_definitions    = templatefile("${path.module}/tasks/task_definition.json", {
    project             = "${var.project}"
    aws_region          = "${var.aws_region}"
    ecr_image_uri       = "${var.ecr_image_uri}"
    TUSHARE_API_TOKEN   = "${var.TUSHARE_API_TOKEN}"
    TG_BOT_API_TOKEN    = "${var.TG_BOT_API_TOKEN}"
    TG_CHAT_IDS         = "${var.TG_CHAT_IDS}"
    PG_DB_URL           = "${var.PG_DB_URL}"
    PG_DB_PWD           = "${var.PG_DB_PWD}"
    ENV                 = "${var.ENV}"
    SMTP_ADDRESS        = "${var.SMTP_ADDRESS}"
    SMTP_PORT           = "${var.SMTP_PORT}"
    SMTP_USERNAME       = "${var.SMTP_USERNAME}"
    SMTP_PASSWORD       = "${var.SMTP_PASSWORD}"
    SMTP_MAIL_FROM      = "${var.SMTP_MAIL_FROM}"
    SMTP_MAIL_FROM_ALIAS = "${var.SMTP_MAIL_FROM_ALIAS}"
  })
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "${var.ecs_cpu_units}"
  memory                   = "${var.ecs_memory}"
  execution_role_arn       = "${aws_iam_role.ecs_task_execution_role.arn}" # This enables the service to e.g. pull the image from ECR, spin up or deregister tasks etc
  task_role_arn            = "${aws_iam_role.ecs_service_role.arn}" # regulates what AWS services the task has access to, e.g. your application is using a DynamoDB, then the task role must give the task access to Dynamo.

  tags = {
    Project     = "${var.project}"
    Environment = "${var.env}"
  }
}

