variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "ami_id" {
  description = "Ubuntu 22.04 LTS AMI ID (region-specific — update for your region)"
  type        = string
  default     = "ami-0f5ee92e2d63afc18" # Ubuntu 22.04 LTS, ap-south-1
}

variable "instance_type" {
  description = "EC2 instance type (free-tier eligible)"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name of an existing EC2 key pair for SSH access"
  type        = string
}

variable "ssh_allowed_cidr" {
  description = "CIDR block allowed to SSH into the instance (restrict to your IP)"
  type        = string
  default     = "0.0.0.0/0"
}
