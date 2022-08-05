
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project}_ecs_cluster_${var.env}"

  tags = {
    Project     = "${var.project}"
    Environment = "${var.env}"
  }

  capacity_providers = ["FARGATE_SPOT"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = "100"
  }
}

data "template_file" "task" {
  template = "${file("./Infrastructure/tf-fargate/tasks/task_definition.json")}"

  vars = {
    project             = "${var.project}"
    aws_region          = "${var.aws_region}"
    ecr_image_uri       = "${var.ecr_image_uri}"
    TUSHARE_API_TOKEN = "${var.TUSHARE_API_TOKEN}"
    TG_BOT_API_TOKEN = "${var.TG_BOT_API_TOKEN}"
    TG_CHAT_IDS = "${var.TG_CHAT_IDS}"
  }
}

resource "aws_ecs_task_definition" "task_definition" {
  family                   = "${var.project}_task_definition_${var.env}"
  container_definitions     = "${data.template_file.task.rendered}"
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

