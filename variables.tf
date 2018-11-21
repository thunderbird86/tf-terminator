variable "name" {
  description = "Name of lambda function"
  default     = "terminator"
}

variable "run_on_regions" {
  description = "The list of AWS regions where to run the schedulers."
  type        = "list"
  default     = [""]
}

variable "scheduler_interval" {
  description = "The interval of execution of the scheduler."
  type        = "string"
  default     = "rate(5 minutes)"
}
