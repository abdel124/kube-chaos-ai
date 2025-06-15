#!/bin/bash
set -euxo pipefail

# Install Docker
yum update -y
yum install -y docker
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && mv kubectl /usr/local/bin/

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
install minikube-linux-amd64 /usr/local/bin/minikube

# Get EC2 public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Start Minikube with Docker driver bound to public IP
su - ec2-user -c "minikube start --driver=docker --apiserver-ips=${PUBLIC_IP} --force"

# Save kubeconfig
su - ec2-user -c "mkdir -p /home/ec2-user/kubeconfig && cp /home/ec2-user/.kube/config /home/ec2-user/kubeconfig/config"
