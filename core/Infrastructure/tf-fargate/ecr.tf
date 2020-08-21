resource "aws_ecr_repository" "ecr" {
  name = "${var.project}-ecr-${var.env}"
  
  tags = {
    Project     = "${var.project}"
    Environment = "${var.env}"
  }
}
