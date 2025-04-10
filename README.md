# 📦 Complete DevOps Project

This project demonstrates how to build, dockerize, and push a simple Python Flask application to AWS Elastic Container Registry (ECR), and deploy it using ECS (Fargate and EC2 launch types), EKS, ArgoCD, and GitHub Actions.

---

## 🧰 Tech Stack & Tools

- Python (Flask)
- Docker
- Git & GitHub
- AWS CLI
- AWS ECR (Elastic Container Registry)
- AWS ECS (Fargate & EC2 Launch Types with ALB)
- AWS EKS (Managed EKS service with node group using eksctl)
- ArgoCD (Automatic Sync to GitHub repo with deployment manifests)
- GitHub Actions (CI/CD for Docker build, push to ECR, deploy with ArgoCD)

---

## 🔤 Application Overview

A simple **Flask application** with the following endpoints:

- `/` – Home route returning a basic response
- `/health` – Health check endpoint to verify the app status

---

## 🔧 Setup Instructions

### ✅ Step 1: Install AWS CLI

```bash
sudo yum install awscli  # For Amazon Linux/CentOS
```

---

## 🧰 Write Basic Python Flask Application with (/, /health) routes.

---

## 🧰 Dockerize the Application

```bash
docker build -t flask-app -f deployments/Dockerfile .
docker images  # Tag the image
```

---

## 🧰 Push Image to ECR

```bash
aws ecr create-repository --repository-name flask-app --region us-east-1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker tag flask-app <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-app
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-app
```

---

## ✅ Deploy to AWS ECS (Fargate)

**Why Fargate?**

- No need to manage servers
- Scales automatically
- Ideal for beginners

**Key Concepts:**

- Task Definition: Blueprint of container (image, port, CPU, memory)
- Service: Ensures desired task count
- Cluster: Logical group to manage services

**Handle Code Changes:**

- Push updated image to ECR
- Create new task definition revision
- Update ECS service to use new revision
- Enable force new deployment

### 🧠 Task Definition Revisions

| Concept               | Reason                                                  |
|----------------------|----------------------------------------------------------|
| Task Definition      | Container blueprint                                      |
| Revisioning          | Version control and rollback                             |
| Force New Deployment | Replace tasks with updated image                         |

---

## ✅ Deploy to AWS ECS (EC2 Launch Type)

1. **ECS Cluster Setup**
   - Created ECS cluster using EC2 launch type
   - Used ECS-optimized Amazon Linux 2 AMI

2. **Task Definition**
   - Pulled container image from ECR
   - Port mapping (5000:5000)
   - CloudWatch logging
   - Networking mode: bridge/AWSVPC

3. **Service Creation & ALB**
   - ECS service with multiple tasks
   - ALB with Target Group and Listener rules

4. **Security & IAM**
   - ALB SG allows traffic to ECS
   - IAM role allows ECS & ECR access

5. **Verification**
   - Access via ALB DNS
   - Confirm routes `/` and `/health`

---

## ✅ Deploy to AWS EKS with eksctl

```bash
eksctl create cluster \
  --name flask-cluster \
  --region us-east-1 \
  --nodegroup-name flask-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3

kubectl get nodes
kubectl get pods --all-namespaces
```

**Expose Flask App**

```bash
kubectl expose deploy flask-app --port 5000 --type=LoadBalancer --name flask-service
```

**Verify Access**

```bash
curl http://<EXTERNAL-IP>:8080
```

---

# 🚀 ArgoCD Setup & GitOps Deployment

## 1️⃣ Install ArgoCD CLI

```bash
curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x argocd
sudo mv argocd /usr/local/bin/
```

## Login to ArgoCD

```bash
kubectl get svc -n argocd
argocd login <ARGOCD_ELB_DNS> --username admin --password <your-password>
# or
kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
```

## Register EKS Cluster

```bash
argocd cluster add arn:aws:eks:us-east-1:<AWS_ACCOUNT_ID>:cluster/<EKS_CLUSTER_NAME>
```

## Create ArgoCD Application

```bash
argocd app create flask-app \
  --repo https://github.com/<your-github-username>/<your-repo> \
  --path k8s-manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --sync-policy automated
```

## Sync, Monitor, and Access ArgoCD

```bash
argocd app sync flask-app
argocd app get flask-app
argocd app list
argocd app delete flask-app
```

Access ArgoCD UI:

```
https://<ARGOCD_ELB_DNS>
```

---

## ✨ CI/CD Pipeline with GitHub Actions & ArgoCD

### 🛠️ Workflow Overview

1. Checkout code
2. Login to AWS
3. Build Docker image
4. Push to ECR
5. Update K8s manifests
6. Commit & Push changes
7. ArgoCD auto-sync

### 📁 GitHub Actions Workflow (Simplified)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ROLE_NAME>
          aws-region: us-east-1

      - name: Log in to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build, Tag, and Push Docker image
        run: |
          IMAGE_TAG=$(date +%s)
          docker build -t <ECR_REPO_URI>:${IMAGE_TAG} .
          docker push <ECR_REPO_URI>:${IMAGE_TAG}

      - name: Update K8s Manifest
        run: |
          sed -i "s|image: .*|image: <ECR_REPO_URI>:${IMAGE_TAG}|" k8s-manifests/deployment.yaml
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add k8s-manifests/deployment.yaml
          git commit -m "Update image to ${IMAGE_TAG}"
          git push
```

---

This complete setup ensures continuous integration and deployment using containerized applications deployed on AWS ECS/EKS with GitOps via ArgoCD.

