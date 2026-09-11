# VULNERABILITY: Hardcoded secrets in Terraform
variable "db_password" {
  default = "SuperSecretDBPassword123!"
}

# VULNERABILITY: Overly permissive security group
resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# VULNERABILITY: S3 bucket without encryption and public access
resource "aws_s3_bucket" "data" {
  bucket = "my-sensitive-data-bucket"

  # No server-side encryption
  # No versioning
  # No logging
}

resource "aws_s3_bucket_acl" "data_acl" {
  bucket = aws_s3_bucket.data.id
  acl    = "public-read"  # Public read access
}

# VULNERABILITY: IAM policy with wildcard permissions
resource "aws_iam_policy" "admin_policy" {
  name        = "admin_policy"
  description = "Overly permissive policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["*"]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

# VULNERABILITY: EC2 instance with SSH open to world
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  # SSH open to world
  vpc_security_group_ids = [aws_security_group.allow_all.id]

  # VULNERABILITY: Root volume not encrypted
  root_block_device {
    volume_size = 8
    encrypted   = false
  }

  # VULNERABILITY: User data with secrets
  user_data = <<-EOF
              #!/bin/bash
              DB_PASSWORD="SuperSecretDBPassword123!"
              echo "Starting application..."
              EOF
}