data "archive_file" "this" {
  type        = "zip"
  source_dir  = "${path.module}/src/terminator/"
  output_path = "${path.module}/src/${local.archived_file}"
}
