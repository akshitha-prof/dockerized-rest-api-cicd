terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
}

# ── Security Group: allow SSH + API port ───────────────────────────────────────
resource "aws_security_group" "task_api_sg" {
  name        = "task-api-sg"
  description = "Allow SSH and API traffic"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  ingress {
    description = "Task API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "task-api-sg"
  }
}

# ── EC2 instance running the Dockerized API ────────────────────────────────────
resource "aws_instance" "task_api" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.task_api_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install -y docker.io docker-compose
              systemctl enable docker
              systemctl start docker
              usermod -aG docker ubuntu
              cd /home/ubuntu
              git clone https://github.com/akshitha-prof/dockerized-rest-api-cicd.git
              cd dockerized-rest-api-cicd
              docker-compose up -d
              EOF

  tags = {
    Name = "task-api-server"
  }
}
