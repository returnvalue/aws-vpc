import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['ProductionVPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']

rts = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
priv_rt = rts['RouteTables'][0]['RouteTableId']

ec2.create_vpc_endpoint(
    VpcId=vpc_id,
    ServiceName='com.amazonaws.us-east-1.s3',
    VpcEndpointType='Gateway',
    RouteTableIds=[priv_rt]
)
