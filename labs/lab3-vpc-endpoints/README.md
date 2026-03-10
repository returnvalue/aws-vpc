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

## 🧠 Key Concepts & Importance

- **Gateway Endpoints:** Specifically for **S3 and DynamoDB**. These modify your route tables to send service traffic through the internal AWS network.
- **Improved Security:** Traffic never traverses the public internet or your NAT Gateway, reducing exposure and potential security risks.
- **Cost Reduction:** Gateway Endpoints are free. By routing S3 traffic through an endpoint, you avoid the **$0.045/GB data processing fee** typically charged by NAT Gateways.
- **Service Specificity:** Endpoints target specific services. Unlike a NAT Gateway which is a general exit point, an endpoint only provides a path to the AWS service named in its configuration.
