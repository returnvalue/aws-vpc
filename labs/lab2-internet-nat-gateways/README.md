# Lab 2: Internet & NAT Gateways

**Goal:** Route 0.0.0.0/0 to an Internet Gateway for the public subnet. Place a NAT Gateway in the public subnet to enable outbound internet access for the private subnet.

```bash
# 1. Create and attach an Internet Gateway
IGW_ID=$(awslocal ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
awslocal ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID

# 2. Configure Public Route Table
PUB_RT=$(awslocal ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
PUB_RT=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
awslocal ec2 create-route --route-table-id $PUB_RT --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
aws ec2 create-route --route-table-id $PUB_RT --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
awslocal ec2 associate-route-table --subnet-id $PUB_SUBNET --route-table-id $PUB_RT
aws ec2 associate-route-table --subnet-id $PUB_SUBNET --route-table-id $PUB_RT

# 3. Create a NAT Gateway for the Private Subnet
EIP_ALLOC=$(awslocal ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
EIP_ALLOC=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
NAT_ID=$(awslocal ec2 create-nat-gateway --subnet-id $PUB_SUBNET --allocation-id $EIP_ALLOC --query 'NatGateway.NatGatewayId' --output text)
NAT_ID=$(aws ec2 create-nat-gateway --subnet-id $PUB_SUBNET --allocation-id $EIP_ALLOC --query 'NatGateway.NatGatewayId' --output text)

# 4. Configure Private Route Table
PRIV_RT=$(awslocal ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
PRIV_RT=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
awslocal ec2 create-route --route-table-id $PRIV_RT --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT_ID
aws ec2 create-route --route-table-id $PRIV_RT --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT_ID
awslocal ec2 associate-route-table --subnet-id $PRIV_SUBNET --route-table-id $PRIV_RT
aws ec2 associate-route-table --subnet-id $PRIV_SUBNET --route-table-id $PRIV_RT
```

## 🧠 Key Concepts & Importance

- **Public Subnet Definition:** A subnet is "public" only if its route table points `0.0.0.0/0` (all internet traffic) to an **Internet Gateway (IGW)**.
- **NAT Gateway Utility:** Instances in private subnets often need internet access for software updates or API calls. A **NAT Gateway** enables this outbound connectivity while keeping the instances unreachable from the public internet.
- **Cost and Scalability:** NAT Gateways are managed by AWS and scale automatically, but they incur hourly and data-processing charges. In large architectures, routing S3/DynamoDB traffic via Endpoints (Lab 3) is a preferred cost-optimization strategy.

## 🛠️ Command Reference

- `ec2 create-internet-gateway`: Creates an Internet Gateway.
- `ec2 attach-internet-gateway`: Attaches an IGW to a VPC.
- `ec2 create-route-table`: Creates a route table.
- `ec2 create-route`: Adds a route to a route table.
    - `--gateway-id`: The ID of an Internet Gateway.
    - `--nat-gateway-id`: The ID of a NAT Gateway.
- `ec2 associate-route-table`: Associates a route table with a subnet.
- `ec2 allocate-address`: Allocates an Elastic IP address, required for a NAT Gateway.
    - `--domain vpc`: Indicates the address is for use in a VPC.
- `ec2 create-nat-gateway`: Creates a NAT Gateway.
    - `--subnet-id`: The public subnet in which to place the NAT Gateway.
    - `--allocation-id`: The allocation ID of the Elastic IP.

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
