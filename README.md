# 📦 Complete DevOps Project

This project demonstrates how to build, dockerize, and push a simple Python Flask application to AWS Elastic Container Registry (ECR) using standard DevOps practices and tools.

---

## 🧰 Tech Stack & Tools

- Python (Flask)
- Docker
- Git & GitHub
- AWS CLI
- AWS ECR (Elastic Container Registry)

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

           docker tag flask-app:latest 329599630566.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest   (Here we are tagging flask-app:latest with ECR_REPO_URI:TAG)

           docker push 329599630566.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest   (This command pushes tagged image to AWS ECR REPO)



      
