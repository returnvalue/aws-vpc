import boto3

elbv2 = boto3.client('elbv2', endpoint_url="http://localhost:4566", region_name="us-east-1")
ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['ProductionVPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']

subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
priv_subnet = next((s['SubnetId'] for s in subnets['Subnets'] if any(t['Key'] == 'Name' and t['Value'] == 'PrivateSubnet' for t in s.get('Tags', []))), subnets['Subnets'][0]['SubnetId'])

analytics_vpc = None
all_vpcs = ec2.describe_vpcs()
for v in all_vpcs['Vpcs']:
    if v.get('CidrBlock') == '10.1.0.0/16':
        analytics_vpc = v['VpcId']
        break
if not analytics_vpc:
    analytics_vpc = vpc_id # fallback

nlb_response = elbv2.create_load_balancer(
    Name='PrivateLinkNLB',
    Type='network',
    Subnets=[priv_subnet]
)
nlb_arn = nlb_response['LoadBalancers'][0]['LoadBalancerArn']

service_response = ec2.create_vpc_endpoint_service_configuration(
    NetworkLoadBalancerArns=[nlb_arn],
    AcceptanceRequired=True
)
service_id = service_response['ServiceConfiguration']['ServiceId']

desc_response = ec2.describe_vpc_endpoint_service_configurations(ServiceIds=[service_id])
service_name = desc_response['ServiceConfigurations'][0]['ServiceName']

subnet_response = ec2.create_subnet(VpcId=analytics_vpc, CidrBlock='10.1.1.0/24')
subnet_id = subnet_response['Subnet']['SubnetId']

ec2.create_vpc_endpoint(
    VpcId=analytics_vpc,
    ServiceName=service_name,
    VpcEndpointType='Interface',
    SubnetIds=[subnet_id]
)
