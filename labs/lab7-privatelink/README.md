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

## 🧠 Key Concepts & Importance

- **Service-Level Sharing:** Unlike VPC Peering or TGW, which expose the **entire network**, **AWS PrivateLink** only exposes a specific service (attached to an NLB).
- **Interface VPC Endpoints:** These place a **Network Interface (ENI)** with a private IP address from your subnet into your VPC, acting as an entry point for the shared service.
- **Unidirectional Connection:** Traffic flows from the consumer to the provider only. The provider cannot initiate connections back to the consumer.
- **Overlapping IPs:** PrivateLink works even if both VPCs have identical IP ranges, as it operates at the service level rather than the network level. This makes it ideal for SaaS providers sharing services with many different customers.

## 🛠️ Command Reference

- `elbv2 create-load-balancer`: Creates a Network Load Balancer (NLB).
    - `--name`: The name of the load balancer.
    - `--type`: The type of load balancer (e.g., `network`).
    - `--subnets`: The subnets to associate with the load balancer.
- `ec2 create-vpc-endpoint-service-configuration`: Creates a VPC endpoint service configuration (the Provider).
    - `--network-load-balancer-arns`: The ARN of the NLB to associate with the service.
    - `--acceptance-required`: Indicates whether requests from consumers to create an endpoint to the service must be accepted.
- `ec2 describe-vpc-endpoint-service-configurations`: Describes the VPC endpoint service configurations.
    - `--service-ids`: The ID(s) of the service configurations to describe.
- `ec2 create-vpc-endpoint`: Creates a VPC endpoint (the Consumer).
    - `--vpc-id`: The VPC in which to create the endpoint.
    - `--service-name`: The name of the service for the endpoint.
    - `--vpc-endpoint-type`: The type of endpoint (e.g., `Interface`).
    - `--subnet-ids`: The subnets in which to create the endpoint network interfaces.
- `ec2 create-subnet`: Creates a subnet within a VPC.
