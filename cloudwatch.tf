resource "aws_cloudwatch_event_rule" "this" {
  name                = "${local.lambda_name}"
  description         = "Rule to trigger ${local.lambda_name} function on a schedule"
  schedule_expression = "${var.scheduler_interval}"
  depends_on          = ["aws_lambda_function.this"]
}

resource "aws_cloudwatch_event_target" "this" {
  rule      = "${aws_cloudwatch_event_rule.this.name}"
  target_id = "${local.lambda_name}"
  arn       = "${aws_lambda_function.this.arn}"
}
