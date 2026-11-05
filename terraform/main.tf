# Per-team storage buckets.
#
# In production these are object-storage buckets. For this exercise they are
# modelled with offline resources so no cloud account is needed:
#   random_id.bucket_suffix  -> the globally-unique suffix in the bucket name
#   terraform_data.bucket    -> the bucket itself (a new name means a new bucket)

resource "random_id" "bucket_suffix" {
  count = length(var.teams)

  byte_length = 4

  keepers = {
    team = var.teams[count.index]
  }
}

locals {
  bucket_names = [
    for i, team in var.teams :
    "${var.bucket_prefix}-${var.environment}-${team}-${random_id.bucket_suffix[i].hex}"
  ]
}

resource "terraform_data" "bucket" {
  count = length(var.teams)

  input = {
    name        = local.bucket_names[count.index]
    team        = var.teams[count.index]
    environment = var.environment
    versioning  = true
  }

  triggers_replace = [local.bucket_names[count.index]]
}
