variable "environment" {
  description = "Deployment environment, used in resource names."
  type        = string
}

variable "bucket_prefix" {
  description = "Prefix for every team bucket name."
  type        = string
  default     = "acme"
}

variable "teams" {
  description = "Teams that get their own storage bucket."
  type        = list(string)
}
