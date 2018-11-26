resource "aws_cloudwatch_event_rule" "dry_run" {
  name                = "${local.lambda_name}-dry-run"
  description         = "Rule to trigger ${local.lambda_name} function on a schedule"
  schedule_expression = "${var.dry_run_scheduler_interval}"
  depends_on          = ["aws_lambda_function.this"]
}

resource "aws_cloudwatch_event_target" "dry_run" {
  rule      = "${aws_cloudwatch_event_rule.dry_run.name}"
  target_id = "${local.lambda_name}-dry-run"
  arn       = "${aws_lambda_function.this.arn}"
  input     = "${data.template_file.dry_run.rendered}"
}

resource "aws_cloudwatch_event_rule" "perfom_action" {
  name                = "${local.lambda_name}-perfom-action"
  description         = "Rule to trigger ${local.lambda_name} function on a schedule"
  schedule_expression = "${var.perfom_action_scheduler_interval}"
  depends_on          = ["aws_lambda_function.this"]
}

resource "aws_cloudwatch_event_target" "perfom_action" {
  rule      = "${aws_cloudwatch_event_rule.perfom_action.name}"
  target_id = "${local.lambda_name}-perfom-action"
  arn       = "${aws_lambda_function.this.arn}"
  input     = "${data.template_file.perfom_action.rendered}"
}
