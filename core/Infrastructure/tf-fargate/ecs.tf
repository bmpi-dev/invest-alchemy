
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project}_ecs_cluster_${var.env}"

  tags = {
    Project     = "${var.project}"
    Environment = "${var.env}"
  }
}

data "template_file" "task" {
  template = "${file("./tf-fargate/tasks/task_definition.json")}"

  vars = {
    project             = "${var.project}"
    aws_region          = "${var.aws_region}"
    ecr_image_uri       = "${var.ecr_image_uri}"
  }
}

resource "aws_ecs_task_definition" "task_definition" {
  family                   = "${var.project}_task_definition_${var.env}"
  container_definitions     = "${data.template_file.task.rendered}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "${var.ecs_cpu_units}"
  memory                   = "${var.ecs_memory}"
  execution_role_arn       = "${var.ecs_taskexec_role}"
  task_role_arn            = "${aws_iam_role.ecs_events_role.arn}"

  tags = {
    Project     = "${var.project}"
    Environment = "${var.env}"
  }
}

