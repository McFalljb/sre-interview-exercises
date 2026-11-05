output "bucket_names" {
  description = "Bucket name for each team."
  value       = terraform_data.bucket[*].output.name
}
