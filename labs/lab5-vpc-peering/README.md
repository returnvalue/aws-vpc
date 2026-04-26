# Lab 5: 1-to-1 Multi-VPC Architecture (VPC Peering)

**Goal:** Create an "Analytics" VPC and establish a private, non-transitive VPC peering connection.
```bash
# 1. Create Analytics VPC
ANALYTICS_VPC=$(awslocal ec2 create-vpc --cidr-block 10.1.0.0/16 --query 'Vpc.VpcId' --output text)
ANALYTICS_VPC=$(aws ec2 create-vpc --cidr-block 10.1.0.0/16 --query 'Vpc.VpcId' --output text)

# 2. Request and Accept VPC Peering
PEER_ID=$(awslocal ec2 create-vpc-peering-connection --vpc-id $VPC_ID --peer-vpc-id $ANALYTICS_VPC --query 'VpcPeeringConnection.VpcPeeringConnectionId' --output text)
PEER_ID=$(aws ec2 create-vpc-peering-connection --vpc-id $VPC_ID --peer-vpc-id $ANALYTICS_VPC --query 'VpcPeeringConnection.VpcPeeringConnectionId' --output text)
awslocal ec2 accept-vpc-peering-connection --vpc-peering-connection-id $PEER_ID
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id $PEER_ID

# 3. Update Route Tables to allow traffic across the peer
awslocal ec2 create-route --route-table-id $PRIV_RT --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id $PEER_ID
aws ec2 create-route --route-table-id $PRIV_RT --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id $PEER_ID
```

## 🧠 Key Concepts & Importance

- **Private Networking:** VPC Peering connects two VPCs over the internal AWS network, making instances in both VPCs reachable to each other using private IP addresses.
- **Non-Transitive Nature:** If VPC A is peered with VPC B, and VPC B is peered with VPC C, VPC A **cannot** communicate with VPC C through VPC B. You would need a direct peer between A and C.
- **CIDR Overlap:** VPCs with overlapping IP address ranges (e.g., both use `10.0.0.0/16`) **cannot** be peered. Planning your IP address space is critical in multi-VPC environments.
- **Bi-Directional Configuration:** Peering requires both a request and an acceptance, and route tables in **both** VPCs must be updated to route traffic to the peer connection.

## 🛠️ Command Reference

- `ec2 create-vpc`: Creates a Virtual Private Cloud (VPC).
- `ec2 create-vpc-peering-connection`: Requests a VPC peering connection between two VPCs.
    - `--vpc-id`: The ID of the requester VPC.
    - `--peer-vpc-id`: The ID of the accepter VPC.
- `ec2 accept-vpc-peering-connection`: Accepts a VPC peering connection request.
    - `--vpc-peering-connection-id`: The ID of the peering connection.
- `ec2 create-route`: Adds a route to a route table.
    - `--route-table-id`: The ID of the route table.
    - `--destination-cidr-block`: The destination traffic range.
    - `--vpc-peering-connection-id`: The ID of the peering connection to route traffic through.

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
