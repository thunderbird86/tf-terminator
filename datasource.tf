data "archive_file" "this" {
  type        = "zip"
  source_dir  = "${path.module}/src/terminator/"
  output_path = "${path.module}/src/${local.archived_file}"
}

data "template_file" "dry_run" {
  template = "${file("${path.module}/user_data/dry_run.json.tmpl")}"

  vars {
    run_on_regions = "${jsonencode(var.run_on_regions)}"
  }
}

data "template_file" "perfom_action" {
  template = "${file("${path.module}/user_data/perfom_action.json.tmpl")}"

  vars {
    run_on_regions = "${jsonencode(var.run_on_regions)}"
  }
}
