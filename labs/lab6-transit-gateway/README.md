# Lab 6: Hub-and-Spoke Topology (AWS Transit Gateway)

**Goal:** Set up a centralized Transit Gateway to route traffic between multiple VPCs, solving the scalability issues of non-transitive VPC peering.

```bash
# 1. Create the Transit Gateway
TGW_ID=$(awslocal ec2 create-transit-gateway --description "Central Hub" --query 'TransitGateway.TransitGatewayId' --output text)

# 2. Create a 3rd VPC (e.g., Shared Services)
SHARED_VPC=$(awslocal ec2 create-vpc --cidr-block 10.2.0.0/16 --query 'Vpc.VpcId' --output text)
SHARED_SUBNET=$(awslocal ec2 create-subnet --vpc-id $SHARED_VPC --cidr-block 10.2.1.0/24 --query 'Subnet.SubnetId' --output text)

# 3. Attach the Production VPC to the Transit Gateway
awslocal ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id $TGW_ID \
  --vpc-id $VPC_ID \
  --subnet-ids $PRIV_SUBNET

# 4. Attach the Shared Services VPC to the Transit Gateway
awslocal ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id $TGW_ID \
  --vpc-id $SHARED_VPC \
  --subnet-ids $SHARED_SUBNET
```
