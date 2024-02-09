resource "random_id" "s3_id" {
  byte_length = 2
}

resource "aws_s3_bucket" "dev_bucket" {
  #   bucket = "test-bucket-${random_id.s3_id.dec}"
  bucket = var.storage_account_name

  #   tags = {
  #       Env = "dev"
  #       Service = "s3"
  #   }
}

resource "port_entity" "aws_s3_bucket" {
  count      = length(aws_s3_bucket.dev_bucket) > 0 ? 1 : 0
  identifier = var.storage_account_name
  title      = var.storage_account_name
  blueprint  = "s3_bucket"
#   run_id     = var.port_run_id
  properties = {
    string_props = {
      "bucket_name" = var.storage_account_name,
      "bucket_acl"  = var.location
    }
  }

  depends_on = [aws_s3_bucket.dev_bucket]
}
