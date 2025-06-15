variable "aws_region" {
  default = "us-west-2"
}

variable "key_name" {
  default = "minikube-auto-key"
}

variable "instance_type" {
  default = "t3.medium"
}

variable "ami_id" {
  # Amazon Linux 2 for us-west-2
  default = "ami-0c55b159cbfafe1f0"
}

variable "my_ip" {
  description = "Your IP address for SSH and Kubernetes API access"
  default     = "YOUR.IP.ADDRESS.HERE/32"
}