###########################################
# PROVIDER
###########################################
provider "aws" {
  region = var.aws_region
}

###########################################
# SSH KEY GENERATION
###########################################
resource "tls_private_key" "minikube" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "minikube_key" {
  key_name   = var.key_name
  public_key = tls_private_key.minikube.public_key_openssh
}

resource "local_file" "private_key" {
  content          = tls_private_key.minikube.private_key_pem
  filename         = "${path.module}/minikube.pem"
  file_permission  = "0400"
}

###########################################
# NETWORKING
###########################################
resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "this" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
}

resource "aws_route_table" "this" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }
}

resource "aws_route_table_association" "this" {
  subnet_id      = aws_subnet.this.id
  route_table_id = aws_route_table.this.id
}

resource "aws_security_group" "minikube_sg" {
  name   = "minikube-sg"
  vpc_id = aws_vpc.this.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  ingress {
    description = "K8s API Access"
    from_port   = 8443
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

###########################################
# EC2 INSTANCE
###########################################
resource "aws_instance" "minikube" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.this.id
  key_name                    = aws_key_pair.minikube_key.key_name
  vpc_security_group_ids      = [aws_security_group.minikube_sg.id]
  associate_public_ip_address = true
  user_data                   = file("user_data.sh")

  tags = {
    Name = "minikube-ec2"
  }
}