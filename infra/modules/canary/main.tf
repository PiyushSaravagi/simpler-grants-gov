#
# Synthetic Canary Resources:
#

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Logging Bucket
resource "aws_s3_bucket" "canary-reports" {
  # contains the zip and the canary logs
  # checkov:skip=CKV_AWS_144: CORS access not relevant to this bucket
  # checkov:skip=CKV2_AWS_62:S3 bucket does not need notifications enabled
  # checkov:skip=CKV_AWS_18:Access logging was not considered necessary for this bucket
  # checkov:skip=CKV2_AWS_61:No need to define S3 bucket lifecycle configuration to expire. Stored files are screenshots and a JSON with a small file size
  bucket = "s3-canaries-reports-${data.aws_caller_identity.current.account_id}"
}
resource "aws_s3_bucket_versioning" "canary-reports" {
  bucket = aws_s3_bucket.canary-reports.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "canary-reports" {
  bucket = aws_s3_bucket.canary-reports.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "canary-reports" {
  bucket = aws_s3_bucket.canary-reports.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.canary-reports.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

# KMS Key to encrypt bucket
resource "aws_kms_key" "canary-reports" {
  description = "KMS key for Synthetics Canary"
  # The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
  deletion_window_in_days = "10"
  # Generates new cryptographic material every 365 days, this is used to encrypt your data. The KMS key retains the old material for decryption purposes.
  enable_key_rotation = "true"
  # checkov:skip=CKV2_AWS_64:TODO: https://github.com/HHS/simpler-grants-gov/issues/2366
}

# Assume role for the canary
resource "aws_iam_role" "canary-role" {
  name               = "canary-role"
  assume_role_policy = data.aws_iam_policy_document.canary-assume-role-policy.json
}
data "aws_iam_policy_document" "canary-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
  }
}

# Attach access policies to canary role
resource "aws_iam_role_policy_attachment" "canary-reports" {
  role       = aws_iam_role.canary-role.name
  policy_arn = aws_iam_policy.canary-reports.arn
}
resource "aws_iam_policy" "canary-reports" {
  name   = "homepage-monitoring"
  policy = data.aws_iam_policy_document.canary-reports.json
}

data "aws_iam_policy_document" "canary-reports" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject", "s3:GetObject"]
    resources = [aws_s3_bucket.canary-reports.arn, "${aws_s3_bucket.canary-reports.arn}/*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["s3:GetBucketLocation"]
    resources = [aws_s3_bucket.canary-reports.arn, "${aws_s3_bucket.canary-reports.arn}/*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents", "logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*"]
  }
  statement {
    effect    = "Allow"
    resources = ["*"]
    actions   = ["cloudwatch:PutMetricData"]
    condition {
      test     = "StringEquals"
      variable = "cloudwatch:namespace"
      values   = ["CloudWatchSynthetics"]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["s3:ListAllMyBuckets", "xray:PutTraceSegments"]
    resources = ["*"]
  }
}

# # Canary code
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "canary_script.py"
  output_path = "python/canary_script.zip"
}

# Canary
resource "aws_synthetics_canary" "canary" {
  name                 = "homepage-monitoring"
  artifact_s3_location = "s3://${aws_s3_bucket.canary-reports.id}/"
  execution_role_arn   = aws_iam_role.canary-role.arn
  runtime_version      = "syn-python-selenium-2.0"
  handler              = "canary_script.handler"
  start_canary         = true
  zip_file             = data.archive_file.lambda.output_path

  success_retention_period = 2
  failure_retention_period = 14

  schedule {
    expression = "rate(5 minutes)"
  }

  run_config {
    timeout_in_seconds = 15
    active_tracing     = false
  }

  tags = {
    Name = "canary"
  }
  depends_on = [aws_s3_bucket.canary-reports]

}
