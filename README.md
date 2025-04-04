# Complete_DevOps_Project
Using Most DevOps Tools to create and deploy this project
  
1) Written a Basic Python Flask Application with (/, /health) routes.

2) Install AWS CLI

3) Dockerize the application

4) Pushed the image to ECR (Elastic Container Registry) 

    steps: aws ecr create-repository --repository-name flask-app --regions us-east-1
     
           aws ecr get-login-password --regions us-east-1 | docker login username AWS --password-stdin 329599630566.dkr.ecr.us-east-1.amazonaws.com/flask-app

           docker build -t flask-app -f deployments/Dockerfile .
        
           docker images  (Lists all images, then we need to tag the locally built image with ecr repo)

           docker tag flask-app:latest 329599630566.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest   (Here we are tagging flask-app:latest with ECR_REPO_URI:TAG)

           docker push 329599630566.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest   (This command pushes tagged image to AWS ECR REPO)



      
