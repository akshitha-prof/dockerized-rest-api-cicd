output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.task_api.public_ip
}

output "api_url" {
  description = "URL to access the deployed API"
  value       = "http://${aws_instance.task_api.public_ip}:8000"
}

output "ssh_command" {
  description = "Command to SSH into the instance"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_instance.task_api.public_ip}"
}
