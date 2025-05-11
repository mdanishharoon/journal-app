variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "journal-app-cluster"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "demo"
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
  default     = "journal-app"  # Updated to match the actual key name in AWS
} 