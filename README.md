# AWS Advanced VPC Architecture Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-VPC_Architecture-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains a comprehensive set of hands-on labs demonstrating advanced Amazon Virtual Private Cloud (VPC) concepts. It bridges the gap between AWS theoretical knowledge (SAA-C03) and practical implementation using [LocalStack Pro](https://localstack.cloud/) to simulate a complete AWS cloud environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS documentation and best practices, these labs walk through the deployment of:
* **Foundational Networking:** Amazon VPC provides an isolated network environment. You have complete control over networking, including IP ranges, subnets, route tables, and gateways. A /24 subnet provides 256 total IP addresses, but AWS reserves 5 IP addresses, leaving 251 available.
* **Routing & Internet Access:** Internet Gateways provide access to the internet, while a NAT Gateway enables outbound internet access for private subnets. Instances in the private subnet remain private with no inbound access from the internet. 
* **Private Connectivity:** VPC Endpoints provide private connectivity to AWS services like S3 and DynamoDB without traversing the internet. 
* **Layered Security:** Security Groups are stateful, meaning if inbound is allowed, return traffic is automatically allowed. Network ACLs are stateless, support Deny rules, and evaluate traffic at the subnet level. Network ACLs do not support rate limiting.
* **Multi-VPC Topologies:** VPC Peering connects two VPCs privately but is not transitive. AWS Transit Gateway acts as a central hub for VPCs and is highly scalable. 
* **Shared Services:** AWS PrivateLink provides private connectivity to services exposed via VPC Endpoint Services without requiring VPC peering or an Internet Gateway.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/awslabs/vpc.git
   cd vpc
   ```

2. Configure your LocalStack Auth Token:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

3. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative, end-to-end scenario rather than isolated tasks. You are building one evolving architecture as you progress.
>
> **Session Persistence:** You must run all commands sequentially within the **same terminal session**. The labs rely on bash variables (like `$VPC_ID`, `$PRIV_RT`, etc.) created in earlier steps. If you close your terminal, these variables will be lost and subsequent labs will fail.

## 📚 Labs Index
1. [Lab 1: Foundational VPC & Subnet Isolation](./labs/lab1-vpc-subnets/README.md)
2. [Lab 2: Internet & NAT Gateways](./labs/lab2-internet-nat-gateways/README.md)
3. [Lab 3: Secure AWS Access via VPC Endpoints](./labs/lab3-vpc-endpoints/README.md)
4. [Lab 4: Defense in Depth (Security Groups vs. NACLs)](./labs/lab4-security-groups-nacls/README.md)
5. [Lab 5: 1-to-1 Multi-VPC Architecture (VPC Peering)](./labs/lab5-vpc-peering/README.md)
6. [Lab 6: Hub-and-Spoke Topology (AWS Transit Gateway)](./labs/lab6-transit-gateway/README.md)
7. [Lab 7: Unidirectional Service Sharing (AWS PrivateLink)](./labs/lab7-privatelink/README.md)

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
