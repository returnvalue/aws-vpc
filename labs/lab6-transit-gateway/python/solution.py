import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['ProductionVPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']

subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
priv_subnet = next(s['SubnetId'] for s in subnets['Subnets'] if any(t['Key'] == 'Name' and t['Value'] == 'PrivateSubnet' for t in s.get('Tags', [])))

tgw_response = ec2.create_transit_gateway(Description='Central Hub')
tgw_id = tgw_response['TransitGateway']['TransitGatewayId']

shared_vpc_response = ec2.create_vpc(CidrBlock='10.2.0.0/16')
shared_vpc = shared_vpc_response['Vpc']['VpcId']

shared_subnet_response = ec2.create_subnet(VpcId=shared_vpc, CidrBlock='10.2.1.0/24')
shared_subnet = shared_subnet_response['Subnet']['SubnetId']

ec2.create_transit_gateway_vpc_attachment(
    TransitGatewayId=tgw_id,
    VpcId=vpc_id,
    SubnetIds=[priv_subnet]
)

ec2.create_transit_gateway_vpc_attachment(
    TransitGatewayId=tgw_id,
    VpcId=shared_vpc,
    SubnetIds=[shared_subnet]
)
