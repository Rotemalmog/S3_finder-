resource "aws_s3_bucket" "images_rotem" {
  bucket = "images_buket"  # S3 bucket name; must be globally unique
  tags = {
    Name        = "images_buket"
    Environment = "test"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.images_rotem.bucket
}
