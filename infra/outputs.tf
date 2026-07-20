output "instance_ip" {
  description = "Public IP of the EC2 app server (Elastic IP)"
  value       = aws_eip.app.public_ip
}

output "db_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "db_host" {
  description = "RDS PostgreSQL hostname (no port)"
  value       = aws_db_instance.postgres.address
}
