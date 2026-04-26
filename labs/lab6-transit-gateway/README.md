# Lab 6: Hub-and-Spoke Topology (AWS Transit Gateway)

**Goal:** Set up a centralized Transit Gateway to route traffic between multiple VPCs, solving the scalability issues of non-transitive VPC peering.
```bash
# 1. Create the Transit Gateway
TGW_ID=$(awslocal ec2 create-transit-gateway --description "Central Hub" --query 'TransitGateway.TransitGatewayId' --output text)
TGW_ID=$(aws ec2 create-transit-gateway --description "Central Hub" --query 'TransitGateway.TransitGatewayId' --output text)

# 2. Create a 3rd VPC (e.g., Shared Services)
SHARED_VPC=$(awslocal ec2 create-vpc --cidr-block 10.2.0.0/16 --query 'Vpc.VpcId' --output text)
SHARED_VPC=$(aws ec2 create-vpc --cidr-block 10.2.0.0/16 --query 'Vpc.VpcId' --output text)
SHARED_SUBNET=$(awslocal ec2 create-subnet --vpc-id $SHARED_VPC --cidr-block 10.2.1.0/24 --query 'Subnet.SubnetId' --output text)
SHARED_SUBNET=$(aws ec2 create-subnet --vpc-id $SHARED_VPC --cidr-block 10.2.1.0/24 --query 'Subnet.SubnetId' --output text)

# 3. Attach the Production VPC to the Transit Gateway
awslocal ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id $TGW_ID \
  --vpc-id $VPC_ID \
  --subnet-ids $PRIV_SUBNET
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id $TGW_ID \
  --vpc-id $VPC_ID \
  --subnet-ids $PRIV_SUBNET

# 4. Attach the Shared Services VPC to the Transit Gateway
awslocal ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id $TGW_ID \
  --vpc-id $SHARED_VPC \
  --subnet-ids $SHARED_SUBNET
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id $TGW_ID \
  --vpc-id $SHARED_VPC \
  --subnet-ids $SHARED_SUBNET
```

## 🧠 Key Concepts & Importance

- **Scalability:** Unlike VPC peering, where you need a unique connection for every pair of VPCs (a "full mesh" is `n*(n-1)/2`), a **Transit Gateway (TGW)** acts as a central hub. It scales easily as you add more VPCs.
- **Transitive Routing:** A TGW allows VPCs to communicate with each other through the hub, solving the non-transitivity issue of peering.
- **Hybrid Cloud:** TGWs can also aggregate VPN and Direct Connect links, enabling easy communication between on-prem data centers and multiple VPCs.
- **Hub-and-Spoke:** This model is the standard for large-scale enterprise deployments on AWS.

## 🛠️ Command Reference

- `ec2 create-transit-gateway`: Creates a Transit Gateway.
    - `--description`: A description of the Transit Gateway.
- `ec2 create-vpc`: Creates a Virtual Private Cloud (VPC).
- `ec2 create-subnet`: Creates a subnet within a VPC.
- `ec2 create-transit-gateway-vpc-attachment`: Attaches a VPC to a Transit Gateway.
    - `--transit-gateway-id`: The ID of the Transit Gateway.
    - `--vpc-id`: The ID of the VPC to attach.
    - `--subnet-ids`: The IDs of the subnets to use for the attachment.

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
