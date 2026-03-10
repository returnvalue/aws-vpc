# AWS Advanced VPC Architecture Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-VPC_Architecture-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains a comprehensive set of hands-on labs demonstrating advanced Amazon Virtual Private Cloud (VPC) concepts. It bridges the gap between AWS theoretical knowledge (SAA-C03) and practical implementation using [LocalStack Pro](https://localstack.cloud/) to simulate a complete AWS cloud environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS documentation and best practices, these labs walk through the deployment of:
* [cite_start]**Foundational Networking:** Amazon VPC provides an isolated network environment. [cite_start]You have complete control over networking, including IP ranges, subnets, route tables, and gateways. [cite_start]A /24 subnet provides 256 total IP addresses, but AWS reserves 5 IP addresses, leaving 251 available.
* [cite_start]**Routing & Internet Access:** Internet Gateways provide access to the internet, while a NAT Gateway enables outbound internet access for private subnets[cite: 299, 301]. [cite_start]Instances in the private subnet remain private with no inbound access from the internet. 
* [cite_start]**Private Connectivity:** VPC Endpoints provide private connectivity to AWS services like S3 and DynamoDB without traversing the internet. 
* [cite_start]**Layered Security:** Security Groups are stateful, meaning if inbound is allowed, return traffic is automatically allowed. [cite_start]Network ACLs are stateless, support Deny rules, and evaluate traffic at the subnet level[cite: 336, 341]. [cite_start]Network ACLs do not support rate limiting[cite: 360, 362].
* [cite_start]**Multi-VPC Topologies:** VPC Peering connects two VPCs privately but is not transitive. [cite_start]AWS Transit Gateway acts as a central hub for VPCs and is highly scalable[cite: 318, 319]. 
* [cite_start]**Shared Services:** AWS PrivateLink provides private connectivity to services exposed via VPC Endpoint Services without requiring VPC peering or an Internet Gateway.
* [cite_start]**Hybrid DNS:** Route 53 Resolver endpoints enable DNS resolution between on-premises networks and AWS VPCs.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Clone this repository:
   ```bash
   git clone [https://github.com/yourusername/aws-localstack-vpc-labs.git](https://github.com/yourusername/aws-localstack-vpc-labs.git)
   cd aws-localstack-vpc-labs