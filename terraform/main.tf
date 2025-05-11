terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"  # Stockholm region
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "journal-app-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-north-1a"]
  private_subnets = ["10.0.1.0/24"]
  public_subnets  = ["10.0.101.0/24"]

  enable_nat_gateway = false  # Save costs by not using NAT gateway
  single_nat_gateway = false

  tags = {
    Environment = "demo"
    Project     = "journal-app"
  }
}

# EC2 Instance for MicroK8s and ArgoCD
resource "aws_instance" "k8s_server" {
  ami           = "ami-02b59c03f7baf2c13"  # Ubuntu 22.04 LTS in eu-north-1
  instance_type = "t3.micro"  # Free tier eligible
  subnet_id     = module.vpc.public_subnets[0]
  associate_public_ip_address = true

  
  vpc_security_group_ids = [aws_security_group.k8s_sg.id]
  
  key_name = var.key_name

  root_block_device {
    volume_size = 8  # Free tier gives 30GB, we'll use 8GB
    volume_type = "gp2"
  }

  tags = {
    Name    = "k8s-server"
    Project = "journal-app"
  }
}

# Security Group for K8s server
resource "aws_security_group" "k8s_sg" {
  name        = "k8s-sg"
  description = "Security group for K8s server"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "k8s-sg"
    Project = "journal-app"
  }
} 