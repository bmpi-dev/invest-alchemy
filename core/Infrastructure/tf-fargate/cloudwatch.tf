resource "aws_cloudwatch_event_rule" "cw_run_task" {
  name                = "${var.project}_run_task_${var.env}"
  description         = "Run ${var.project} on ${var.schedule}"
  schedule_expression = "${var.schedule}"
}

resource "aws_cloudwatch_event_target" "cw_event_target" {
  target_id   = "${var.project}_event_target_${var.env}"
  arn         = "${aws_ecs_cluster.ecs_cluster.arn}"
  rule        = "${aws_cloudwatch_event_rule.cw_run_task.name}"
  role_arn    = "${aws_iam_role.ecs_events_role.arn}"

  ecs_target {
      launch_type           = "FARGATE"
      platform_version      = "LATEST"
      task_definition_arn    = "${aws_ecs_task_definition.task_definition.arn}"

      network_configuration {
        subnets             = "${aws_default_subnet.default_az1.*.id}"
        security_groups     = "${var.security_groups_ids}"
        assign_public_ip    = "${var.assign_public_ip}"
      }
  }
}

resource "aws_cloudwatch_log_group" "cw_run_task_log_group" {
  name = "/ecs/${var.project}-fargate-task-definition"

  tags = {
    Environment = "${var.env}"
    Application = "${var.project}"
  }
}