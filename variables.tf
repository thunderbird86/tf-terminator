variable "name" {
  description = "Name of lambda function"
  default     = "terminator"
}

variable "run_on_regions" {
  description = "The list of AWS regions where to run the schedulers."
  type        = list(string)
  default     = [""]
}

variable "dry_run_scheduler_interval" {
  description = "The interval of execution of the scheduler."
  type        = string
  default     = "cron(0 15 * * ? *)"
}

variable "perfom_action_scheduler_interval" {
  description = "The interval of execution of the scheduler."
  type        = string
  default     = "cron(0 18 * * ? *)"
}
