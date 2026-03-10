# Lab 3: Secure AWS Access via VPC Endpoints

**Goal:** Create a Gateway Endpoint to route traffic to S3 directly over the AWS network, bypassing the NAT Gateway.

```bash
# Create a Gateway Endpoint for S3 and associate it with the Private Route Table
awslocal ec2 create-vpc-endpoint \
  --vpc-id $VPC_ID \
  --service-name com.amazonaws.us-east-1.s3 \
  --vpc-endpoint-type Gateway \
  --route-table-ids $PRIV_RT
```
