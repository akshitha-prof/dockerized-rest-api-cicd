# Cloud Deployment Guide

This guide covers deploying the Task Manager API to **AWS EC2** or **GCP Compute Engine** (both free-tier eligible).

---

## Prerequisites

- AWS or GCP account (free tier)
- Docker installed on your VM
- This repo cloned on the VM

---

## AWS EC2 Deployment

### 1. Launch an EC2 Instance
- Go to EC2 → Launch Instance
- Choose: **Ubuntu 22.04 LTS** (t2.micro — free tier)
- Create or select a key pair (download `.pem` file)
- Under **Security Group**, add inbound rules:
  - SSH: port 22 (your IP)
  - HTTP: port 8000 (anywhere — 0.0.0.0/0)

### 2. SSH into the Instance
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 3. Install Docker on Ubuntu
```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
newgrp docker
```

### 4. Clone and Run
```bash
git clone https://github.com/akshitha-prof/dockerized-rest-api-cicd.git
cd dockerized-rest-api-cicd
docker-compose up -d
```

### 5. Verify
```bash
curl http://<EC2_PUBLIC_IP>:8000/health
# → {"status":"healthy","timestamp":"..."}
```

---

## GCP Compute Engine Deployment

### 1. Create a VM Instance
- Go to Compute Engine → VM Instances → Create Instance
- Machine type: **e2-micro** (free tier)
- Boot disk: **Ubuntu 22.04 LTS**
- Firewall: check **Allow HTTP traffic** and add a firewall rule for port 8000

### 2. SSH via Browser or gcloud CLI
```bash
gcloud compute ssh <INSTANCE_NAME> --zone=<YOUR_ZONE>
```

### 3. Install Docker
```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

### 4. Clone and Run
```bash
git clone https://github.com/akshitha-prof/dockerized-rest-api-cicd.git
cd dockerized-rest-api-cicd
docker-compose up -d
```

### 5. Add Firewall Rule for Port 8000
```bash
gcloud compute firewall-rules create allow-task-api \
  --allow tcp:8000 \
  --target-tags http-server
```

### 6. Verify
```bash
curl http://<EXTERNAL_IP>:8000/health
```

---

## Networking Concepts Applied

| Concept | Where Used |
|---|---|
| TCP/IP | All HTTP traffic runs over TCP |
| HTTP/HTTPS | REST API endpoints |
| Firewall rules / Security Groups | Port 8000 opened for inbound traffic |
| DNS | Map your domain to EC2/GCP external IP via A record |
| Load balancing | Add AWS ALB or GCP Load Balancer in front of the container |

---

## Setting Up Docker Hub Secrets (for CI/CD)

In your GitHub repo → Settings → Secrets → Actions, add:
- `DOCKER_USERNAME` — your Docker Hub username
- `DOCKER_PASSWORD` — your Docker Hub access token

On every push to `main`, the pipeline will:
1. Run all pytest cases
2. Build the Docker image
3. Push to Docker Hub automatically
