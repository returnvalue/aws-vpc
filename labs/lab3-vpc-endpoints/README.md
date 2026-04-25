# Lab 3: Secure AWS Access via VPC Endpoints

**Goal:** Create a Gateway Endpoint to route traffic to S3 directly over the AWS network, bypassing the NAT Gateway.

```bash
# Create a Gateway Endpoint for S3 and associate it with the Private Route Table
awslocal ec2 create-vpc-endpoint \
  --vpc-id $VPC_ID \
  --service-name com.amazonaws.us-east-1.s3 \
  --vpc-endpoint-type Gateway \
  --route-table-ids $PRIV_RT
aws ec2 create-vpc-endpoint \
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

## 🛠️ Command Reference

- `ec2 create-vpc-endpoint`: Creates a VPC endpoint.
    - `--vpc-id`: The ID of the VPC.
    - `--service-name`: The service name (e.g., `com.amazonaws.us-east-1.s3`).
    - `--vpc-endpoint-type`: The type of endpoint (e.g., `Gateway`).
    - `--route-table-ids`: The route table(s) to associate with the Gateway endpoint.

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
