output "ec2_public_ip" {
  value = aws_instance.minikube.public_ip
}

output "private_key_file" {
  value = local_file.private_key.filename
}

output "ssh_command" {
  value = "ssh -i minikube.pem ec2-user@${aws_instance.minikube.public_ip}"
}  