# Lab 5: 1-to-1 Multi-VPC Architecture (VPC Peering)

**Goal:** Create an "Analytics" VPC and establish a private, non-transitive VPC peering connection.

```bash
# 1. Create Analytics VPC
ANALYTICS_VPC=$(awslocal ec2 create-vpc --cidr-block 10.1.0.0/16 --query 'Vpc.VpcId' --output text)

# 2. Request and Accept VPC Peering
PEER_ID=$(awslocal ec2 create-vpc-peering-connection --vpc-id $VPC_ID --peer-vpc-id $ANALYTICS_VPC --query 'VpcPeeringConnection.VpcPeeringConnectionId' --output text)
awslocal ec2 accept-vpc-peering-connection --vpc-peering-connection-id $PEER_ID

# 3. Update Route Tables to allow traffic across the peer
awslocal ec2 create-route --route-table-id $PRIV_RT --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id $PEER_ID
```
