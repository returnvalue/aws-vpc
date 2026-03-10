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
* **Hybrid DNS:** Route 53 Resolver endpoints enable DNS resolution between on-premises networks and AWS VPCs.

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