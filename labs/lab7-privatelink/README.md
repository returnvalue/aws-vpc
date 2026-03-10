# Lab 7: Unidirectional Service Sharing (AWS PrivateLink)

**Goal:** Share a service using an Interface VPC Endpoint without exposing the networks to each other via peering.

```bash
# 1. Create a Network Load Balancer (NLB) in the Provider VPC
NLB_ARN=$(awslocal elbv2 create-load-balancer --name PrivateLinkNLB --type network --subnets $PRIV_SUBNET --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# 2. Create a VPC Endpoint Service (The Provider)
SERVICE_ID=$(awslocal ec2 create-vpc-endpoint-service-configuration --network-load-balancer-arns $NLB_ARN --acceptance-required --query 'ServiceConfiguration.ServiceId' --output text)
SERVICE_NAME=$(awslocal ec2 describe-vpc-endpoint-service-configurations --service-ids $SERVICE_ID --query 'ServiceConfigurations[0].ServiceName' --output text)

# 3. Create an Interface Endpoint (The Consumer) in the Analytics VPC
awslocal ec2 create-vpc-endpoint \
  --vpc-id $ANALYTICS_VPC \
  --service-name $SERVICE_NAME \
  --vpc-endpoint-type Interface \
  --subnet-ids $(awslocal ec2 create-subnet --vpc-id $ANALYTICS_VPC --cidr-block 10.1.1.0/24 --query 'Subnet.SubnetId' --output text)
```
