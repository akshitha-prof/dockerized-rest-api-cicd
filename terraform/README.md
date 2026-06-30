# Infrastructure as Code (Terraform)

Provisions an AWS EC2 instance, security group, and bootstraps Docker + the Task API automatically via `user_data` — fully automated infrastructure provisioning with no manual console steps.

## Prerequisites

```bash
# Install Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Configure AWS credentials
aws configure
```

## Usage

```bash
cd terraform

terraform init
terraform plan -var="key_name=your-ec2-keypair-name"
terraform apply -var="key_name=your-ec2-keypair-name"
```

## What gets provisioned

- **Security Group** — opens port 22 (SSH) and port 8000 (API), denies everything else by default
- **EC2 instance** (t2.micro, free-tier) — Ubuntu 22.04
- **User data script** — installs Docker, clones this repo, and runs `docker-compose up -d` automatically on first boot

## Outputs

After `terraform apply`, Terraform prints:
- The instance's public IP
- The live API URL
- The exact SSH command to connect

## Tear down

```bash
terraform destroy -var="key_name=your-ec2-keypair-name"
```

## What this demonstrates

- Infrastructure as Code — repeatable, version-controlled cloud provisioning instead of manual console clicks
- Security group / firewall rule definition as code
- Automated bootstrapping (Docker install + app deployment) via `user_data`
- Terraform state, plan, and apply workflow
