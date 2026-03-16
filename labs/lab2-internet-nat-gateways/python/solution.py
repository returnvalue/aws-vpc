import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['ProductionVPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']

subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
pub_subnet = next(s['SubnetId'] for s in subnets['Subnets'] if any(t['Key'] == 'Name' and t['Value'] == 'PublicSubnet' for t in s.get('Tags', [])))
priv_subnet = next(s['SubnetId'] for s in subnets['Subnets'] if any(t['Key'] == 'Name' and t['Value'] == 'PrivateSubnet' for t in s.get('Tags', [])))

igw_response = ec2.create_internet_gateway()
igw_id = igw_response['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)

pub_rt_response = ec2.create_route_table(VpcId=vpc_id)
pub_rt = pub_rt_response['RouteTable']['RouteTableId']
ec2.create_route(RouteTableId=pub_rt, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
ec2.associate_route_table(SubnetId=pub_subnet, RouteTableId=pub_rt)

alloc_response = ec2.allocate_address(Domain='vpc')
eip_alloc = alloc_response['AllocationId']

nat_response = ec2.create_nat_gateway(SubnetId=pub_subnet, AllocationId=eip_alloc)
nat_id = nat_response['NatGateway']['NatGatewayId']

priv_rt_response = ec2.create_route_table(VpcId=vpc_id)
priv_rt = priv_rt_response['RouteTable']['RouteTableId']
ec2.create_route(RouteTableId=priv_rt, DestinationCidrBlock='0.0.0.0/0', NatGatewayId=nat_id)
ec2.associate_route_table(SubnetId=priv_subnet, RouteTableId=priv_rt)
