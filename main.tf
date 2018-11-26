resource "aws_lambda_function" "this" {
  function_name    = "${local.lambda_name}"
  description      = "Terminate resources based on tags."
  role             = "${aws_iam_role.this.arn}"
  handler          = "terminator.lambda_handler"
  runtime          = "python3.7"
  memory_size      = "128"
  timeout          = "240"
  filename         = "${data.archive_file.this.output_path}"
  source_code_hash = "${data.archive_file.this.output_base64sha256}"
  tags             = "${local.tags}"

  environment {
    variables {
      RUN_ON_REGIONS = "${join(",", var.run_on_regions)}"
    }
  }

  depends_on = ["data.archive_file.this"]
}

locals {
  archived_file = "terminator.zip"
  lambda_name   = "${var.name}"

  tags = {
    Name      = "${local.lambda_name}"
    Terraform = "True"
  }
}
