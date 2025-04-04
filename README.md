# 📦 Complete DevOps Project

This project demonstrates how to build, dockerize, and push a simple Python Flask application to AWS Elastic Container Registry (ECR) using standard DevOps practices and tools.

---

## 🧰 Tech Stack & Tools

- Python (Flask)
- Docker
- Git & GitHub
- AWS CLI
- AWS ECR (Elastic Container Registry)
- AWS ECS (Fargate & EC2 Launch Types.(With ALB))

---

## 🖥️ Application Overview

A simple **Flask application** with the following endpoints:

- `/` – Home route returning a basic response
- `/health` – Health check endpoint to verify the app status

---

## 🔧 Setup Instructions

### ✅ Step 1: Install AWS CLI

If not already installed:

sudo yum install awscli  # For Amazon Linux/CentOS

  
## 🧰 Written a Basic Python Flask Application with (/, /health) routes.

## 🧰  Dockerize the application

## 🧰 Pushed the image to ECR (Elastic Container Registry) 

    ### ✅ Steps: aws ecr create-repository --repository-name flask-app --regions us-east-1
     
           aws ecr get-login-password --regions us-east-1 | docker login username AWS --password-stdin 329599630566.dkr.ecr.us-east-1.amazonaws.com/flask-app

           docker build -t flask-app -f deployments/Dockerfile .
        
           docker images  (Lists all images, then we need to tag the locally built image with ecr repo)


## 🧰✅ Step 2: Deploy to AWS ECS (Fargate)
Service Used: ECS (with Fargate launch type)

**Why Fargate?**

    No need to manage servers
    
    Scales automatically
    
    Ideal for getting started with containers on AWS

**Key Concepts:**

    Task Definition: Blueprint of container (image, port, CPU, memory)
    
    Service: Ensures desired count of tasks are running
    
    Cluster: Logical group to manage services

## 🧰✅ Step 3: Handle Code Changes (New Image Versions)
Problem: ECS won’t automatically use the new image from ECR when you push updates

**Solution:**

    Push the updated image to ECR
    
    Create a new task definition revision
    
    Update the ECS service to use the new revision
    
    Enable force new deployment

**Why: ECS tasks are immutable and tied to specific task definitions**

### 🧠 Theory Behind Revisions

| Concept               | Reason                                                                 |
|------------------------|------------------------------------------------------------------------|
| **Task Definition**    | Ensures consistency in deployments; acts as a container blueprint       |
| **Revisioning**        | Allows version control and rollback by tracking changes                 |
| **Force New Deployment** | Replaces running tasks with new ones using the updated image             |



## ✅Deploying Flask App on ECS with EC2 Launch Type**

## 🧰✅ 1. ECS Cluster Setup
Created an ECS Cluster with EC2 launch type (not Fargate).

Used ECS-optimized Amazon Linux 2 AMI for EC2 instances.

## 🧰✅ 2. Task Definition
Defined a new task definition specifying:

Container Image: Pulled from AWS ECR

Port Mapping: Exposed necessary ports (e.g., 5000:5000)

Log Configuration: Enabled AWS CloudWatch logging

Networking Mode: Bridge/AWSVPC

## 🧰✅ 3. Service Creation & Load Balancer (ALB)
Created an ECS Service running multiple tasks for high availability.

Placed an Application Load Balancer (ALB) in front of the service.

Configured Target Groups & Listeners to route traffic from ALB to ECS tasks.

## 🧰✅ 4. Security & IAM Considerations
Allowed ALB security group to route traffic to ECS tasks.

Ensured EC2 instances have proper IAM roles for ECS & ECR access.

## 🧰✅ 5. Verification & Testing
Accessed the app via ALB DNS Name instead of EC2 public IP.

Verified app functionality with / and /health routes.


## ✅** Deploying a Flask App on AWS EKS**

**Create an EKS Cluster**

eksctl create cluster --name flask-cluster --region us-east-1 --nodegroup-name flask-nodes --node-type t3.medium --nodes 2 --nodes-min 1 --nodes-max 3

**Verify Cluster**

kubectl get nodes
kubectl get pods --all-namespaces

**Exposing the Flask App with a LoadBalancer Service**

kubectl expose deploy flask-app --port 5000 --type=LoadBalancer --name flask-service

🧰✅ **Verifying Access**

curl http://<EXTERNAL-IP>:8080  (Here external IP is AWS ALB DNS name)


