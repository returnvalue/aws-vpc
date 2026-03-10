# Lab 2: Internet & NAT Gateways

**Goal:** Route 0.0.0.0/0 to an Internet Gateway for the public subnet. Place a NAT Gateway in the public subnet to enable outbound internet access for the private subnet.

```bash
# 1. Create and attach an Internet Gateway
IGW_ID=$(awslocal ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
awslocal ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID

# 2. Configure Public Route Table
PUB_RT=$(awslocal ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
awslocal ec2 create-route --route-table-id $PUB_RT --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
awslocal ec2 associate-route-table --subnet-id $PUB_SUBNET --route-table-id $PUB_RT

# 3. Create a NAT Gateway for the Private Subnet
EIP_ALLOC=$(awslocal ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
NAT_ID=$(awslocal ec2 create-nat-gateway --subnet-id $PUB_SUBNET --allocation-id $EIP_ALLOC --query 'NatGateway.NatGatewayId' --output text)

# 4. Configure Private Route Table
PRIV_RT=$(awslocal ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
awslocal ec2 create-route --route-table-id $PRIV_RT --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT_ID
awslocal ec2 associate-route-table --subnet-id $PRIV_SUBNET --route-table-id $PRIV_RT
```

## 🧠 Key Concepts & Importance

- **Public Subnet Definition:** A subnet is "public" only if its route table points `0.0.0.0/0` (all internet traffic) to an **Internet Gateway (IGW)**.
- **NAT Gateway Utility:** Instances in private subnets often need internet access for software updates or API calls. A **NAT Gateway** enables this outbound connectivity while keeping the instances unreachable from the public internet.
- **Cost and Scalability:** NAT Gateways are managed by AWS and scale automatically, but they incur hourly and data-processing charges. In large architectures, routing S3/DynamoDB traffic via Endpoints (Lab 3) is a preferred cost-optimization strategy.
