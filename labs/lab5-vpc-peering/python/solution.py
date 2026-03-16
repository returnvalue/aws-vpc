import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['ProductionVPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']

rts = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
priv_rt = rts['RouteTables'][0]['RouteTableId']

analytics_response = ec2.create_vpc(CidrBlock='10.1.0.0/16')
analytics_vpc = analytics_response['Vpc']['VpcId']

peer_response = ec2.create_vpc_peering_connection(
    VpcId=vpc_id,
    PeerVpcId=analytics_vpc
)
peer_id = peer_response['VpcPeeringConnection']['VpcPeeringConnectionId']

ec2.accept_vpc_peering_connection(VpcPeeringConnectionId=peer_id)

ec2.create_route(
    RouteTableId=priv_rt,
    DestinationCidrBlock='10.1.0.0/16',
    VpcPeeringConnectionId=peer_id
)
