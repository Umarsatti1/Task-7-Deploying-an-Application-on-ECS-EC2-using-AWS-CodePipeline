# Task 7: Deploying an Application on ECS EC2 using AWS CodePipeline

---

## AWS Services Used

The following AWS services were utilized to set up the ECS EC2-based CI/CD pipeline with an Application Load Balancer:

- **Amazon VPC** – For creating public and private subnets, route tables, NAT and Internet gateways.  
- **EC2** – Public Bastion host and private ECS container instances.  
- **ECR (Elastic Container Registry)** – Store Docker images.  
- **ECS (Elastic Container Service)** – ECS Cluster, Task Definitions, and ECS Services.  
- **Application Load Balancer (ALB)** – Distribute traffic across ECS EC2 instances.  
- **Security Groups** – Control inbound and outbound traffic.  
- **IAM** – Roles for CodeBuild, CodePipeline, and ECS Task Execution.  
- **CloudWatch Logs** – Store build and application logs.  
- **S3** – Artifact storage for CodePipeline.  
- **CodeBuild** – Build Docker images, push to ECR, generate deployment artifacts.  
  - Uses a `buildspec.yml` file stored in the project directory.  
- **CodePipeline** – Orchestrate CI/CD: GitHub → CodeBuild → ECS deployment.  
- **GitHub** – Source repository for the Flask application code.  

---

## Task Description

Set up **AWS CodePipeline** on the AWS console for CI/CD of an application running on **ECS EC2** with an **Application Load Balancer (ALB)**.  

---

## Architecture Diagram

<p align="center">
  <img src="./diagram/Architecture Diagram.png" alt="Architecture Diagram" width="850">
</p>

---

## Tasks

### Task 1.1: Create VPC
A **Virtual Private Cloud (VPC)** is a logically isolated network within AWS for secure infrastructure deployment.  

**Steps:**
1. Sign in to AWS Console → VPC → Your VPCs → Create VPC.  
2. Select **VPC Only** and choose a Name and IPv4 CIDR: `10.0.0.0/16` 

**Purpose:** Controls IP range, subnets, routing, and security for both public and private resources.

---

### Task 1.2: Create Internet Gateway
An **Internet Gateway (IGW)** allows VPC resources to communicate with the internet.  

**Steps:**
1. VPC Console → Internet Gateways → Create internet gateway.  
2. Choose a Name and attach it to the VPC.  

---

### Task 1.3: Create NAT Gateway
A **NAT Gateway** provides outbound internet access for private instances without inbound exposure.  

**Steps:**
1. VPC Console → NAT Gateways → Create NAT gateway.  
2. Select **Public Subnet**, assign **Elastic IP** and Name.  

**Note:** For high availability, deploy NAT Gateways in multiple AZs; here, one is sufficient.  

---

### Task 1.4: Create Subnets
**Subnets created:**
- **Public Subnet A:** `10.0.1.0/24`  
- **Public Subnet B:** `10.0.2.0/24`  
- **Private Subnet A:** `10.0.3.0/24`  
- **Private Subnet B:** `10.0.4.0/24`  

**Purpose:** Public subnets host internet-facing resources (ALB, Bastion Host); private subnets host ECS EC2 instances.  

---

### Task 1.5: Create Route Tables
**Route Tables:**
- **Public:** directs traffic to IGW  
- **Private:** directs traffic to NAT Gateway  

---

### Task 1.6: Set Up Routes for Route Tables
**Routes configured:**
- Public: `0.0.0.0/0 → Internet Gateway`
- Private: `0.0.0.0/0 → NAT Gateway`  

---

### Task 1.7: Route Table Association
Associates subnets to their respective route tables:
- Public subnets → Public Route Table  
- Private subnets → Private Route Table  

---

### Task 1.8: Security Groups
Defines network access rules.  

**Examples:**
- `ALB-SG`: HTTP 80 from all  
- `Bastion-SG`: SSH 22 from personal IP  
- `ECS-SG`: HTTP 80/5000 from ALB, SSH 22 from Bastion  

---

### Task 1.9: Public EC2 Instance
**Bastion Host EC2**
- AMI: Amazon Linux 2023, t3.micro  
- Key Pair: `keypair.pem`  
- Public subnet, security group `Bastion-SG`  

**Purpose:** SSH access to private EC2 instances.  

---

### Task 1.10: ECR
**Steps:**
1. Create a Private ECR repository 
2. Push Docker image from local machine to ECR  

---

### Task 1.11: ECS Cluster
**Cluster:** 
- Launch type: EC2  
- Auto Scaling: 2 EC2 instances in private subnets  
- Security group: `ECS-SG`  

**Purpose:** Runs containerized application tasks on private EC2 instances.  

---

### Task 1.12: Test Private EC2 Instances
**SSH into private instances via Bastion Host**  
**Verification:** Docker and ECS agent running, ECS configuration file correct.

---

### Task 1.13: ECS Task Definition
**Task Definition:** 
- Container: Flask app  
- Image: ECR Repository  
- Ports: 5000 (host & container)  
- IAM Role: `ecsTaskExecutionRole`  

---

### Task 1.14: Application Load Balancer and Target Groups
**ALB:** Internet-facing, public subnets  
**Target Group:** `ecs-target-group` → Private EC2 instances port 5000  

---

### Task 1.15: ECS Service
**Service:** `ecs-ec2-task-definition-service`  
- Desired tasks: 2  
- Rolling updates enabled  
- Integrated with ALB for traffic distribution  

---

### Task 1.16: CodeBuild
**Project:** `EC2-ECS-CodeBuild`  
- Source: GitHub repo  
- Privileged mode: Enabled for Docker  
- VPC: Private subnets  
- Output artifact: `imagedefinitions.json`  

**Buildspec File:**  
- A `buildspec.yml` file is stored in the project directory.  
- This file is used by CodeBuild to automate the following steps:
  - Authenticate to Amazon ECR  
  - Build the Docker image  
  - Tag the Docker image  
  - Push the Docker image to ECR  
  - Generate `imagedefinitions.json` for CodePipeline and ECS deployment  

**Purpose:** The buildspec ensures that any code changes pushed to GitHub automatically trigger a Docker image build, push it to ECR, and create deployment artifacts for CodePipeline. 

---

### Task 1.17: CodePipeline
**Pipeline:** `EC2-ECS-Pipeline`  
- Source: GitHub  
- Build: CodeBuild  
- Deploy: ECS Service  
- Automatic rolling deployments  

---

### Task 1.18: End-to-End Testing
- Updated app → GitHub push → CodePipeline triggers → ECS rolling update → ALB serves new version  
- Confirms CI/CD workflow operational  

---

### Task 1.19: IAM Roles, CloudWatch Logs, and S3 Bucket
**Roles:**
- `CodeBuildServiceRole` → Build & push Docker images  
- `AWSCodePipelineServiceRole` → Orchestrates pipeline  
- `ecsTaskExecutionRole` → ECS task permissions  

**CloudWatch Logs:** `/aws/codebuild/...`, `/ecs/...`  
**S3 Bucket:** Stores source & build artifacts  

---

### Task 1.20: Troubleshooting and Lessons Learned
**Issue 1:** Incorrect host port mapping → Fixed host port 5000 & target type “Instances”  
**Issue 2:** ECR login failure → Added permissions to CodePipeline role  
**Issue 3:** Docker build fails in CodeBuild → Enabled Privileged Mode  

---

## Conclusion

The project demonstrates an end-to-end **CI/CD pipeline** using **AWS ECS EC2**, **CodePipeline**, **CodeBuild**, **ECR**, and **ALB**.  
It follows best practices for network segmentation, security, automated deployments, and rolling updates.  

---

