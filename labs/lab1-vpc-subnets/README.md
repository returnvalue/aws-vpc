# Lab 1: Foundational VPC & Subnet Isolation

**Goal:** Create a custom VPC and partition it into public and private subnets. Demonstrate subnet sizing where a /24 subnet yields 251 usable IPs.
```bash
# 1. Create the VPC (10.0.0.0/16)
VPC_ID=$(awslocal ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
awslocal ec2 create-tags --resources $VPC_ID --tags Key=Name,Value=ProductionVPC
aws ec2 create-tags --resources $VPC_ID --tags Key=Name,Value=ProductionVPC

# 2. Create a Public Subnet (10.0.1.0/24)
PUB_SUBNET=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --query 'Subnet.SubnetId' --output text)
PUB_SUBNET=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --query 'Subnet.SubnetId' --output text)
awslocal ec2 create-tags --resources $PUB_SUBNET --tags Key=Name,Value=PublicSubnet
aws ec2 create-tags --resources $PUB_SUBNET --tags Key=Name,Value=PublicSubnet

# 3. Create a Private Subnet (10.0.2.0/24)
PRIV_SUBNET=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --query 'Subnet.SubnetId' --output text)
PRIV_SUBNET=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --query 'Subnet.SubnetId' --output text)
awslocal ec2 create-tags --resources $PRIV_SUBNET --tags Key=Name,Value=PrivateSubnet
aws ec2 create-tags --resources $PRIV_SUBNET --tags Key=Name,Value=PrivateSubnet
```

## 🧠 Key Concepts & Importance

- **VPC CIDR Selection:** Choosing a `/16` block provides 65,536 IP addresses, offering enough headroom for future expansion.
- **Subnet Sizing:** A `/24` subnet provides 256 addresses. However, AWS reserves 5 addresses (Network, VPC Router, DNS, Reserved, Broadcast), leaving you with **251 usable IPs**.
- **Isolation by Default:** Subnets are isolated within the VPC until route tables are explicitly configured. Creating public and private subnets is the industry standard for securing "three-tier" web architectures.

## 🛠️ Command Reference

- `ec2 create-vpc`: Creates a Virtual Private Cloud.
    - `--cidr-block`: The IP range for the VPC.
- `ec2 create-tags`: Adds tags to a resource.
    - `--resources`: The ID(s) of the resource(s) to tag.
    - `--tags`: The key-value pairs for the tags.
- `ec2 create-subnet`: Creates a subnet within a VPC.
    - `--vpc-id`: The VPC ID.
    - `--cidr-block`: The IP range for the subnet.

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
