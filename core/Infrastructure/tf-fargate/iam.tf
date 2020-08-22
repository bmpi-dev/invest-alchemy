######################### Role used by the container regulates what AWS services the task has access to, e.g. your application is using a DynamoDB, then the task role must give the task access to Dynamo.
resource "aws_iam_role" "ecs_service_role" {
  name               = "${var.project}_ecs_service_role_${var.env}"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_service_assume_role_policy.json}"
}

resource "aws_iam_role_policy" "ecs_service_policy" {
  name   = "${var.project}_ecs_service_role_policy_${var.env}"
  policy = "${data.aws_iam_policy_document.ecs_service_policy.json}"
  role   = "${aws_iam_role.ecs_service_role.id}"
}

data "aws_iam_policy_document" "ecs_service_policy" {
  statement {
    effect = "Allow"
    resources = ["*"]
    actions = [
        "iam:ListPolicies",
        "iam:GetPolicyVersion"
    ]
  }
}

data "aws_iam_policy_document" "ecs_service_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_service_role_policy_attachment" {
  role       = aws_iam_role.ecs_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess" # https://gist.github.com/gene1wood/55b358748be3c314f956
}

######################### Role used by the container enables the service to e.g. pull the image from ECR, spin up or deregister tasks etc

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project}_ecs_task_execution_role_${var.env}"
 
  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}
 
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy_attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy" # https://gist.github.com/gene1wood/55b358748be3c314f956
}

######################### Role used for ECS Events

resource "aws_iam_role" "ecs_events_role" {
  name               = "${var.project}_ecs_events_role_${var.env}"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_events_assume_role_policy.json}"
}

resource "aws_iam_role_policy_attachment" "ecs_events_role_policy" {
  policy_arn = "${data.aws_iam_policy.ecs_events_policy.arn}"
  role       = "${aws_iam_role.ecs_events_role.id}"
}

data "aws_iam_policy" "ecs_events_policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceEventsRole" # https://gist.github.com/gene1wood/55b358748be3c314f956
}

data "aws_iam_policy_document" "ecs_events_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

