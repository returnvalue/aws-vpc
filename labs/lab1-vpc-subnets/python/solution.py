import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = vpc_response['Vpc']['VpcId']
ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'ProductionVPC'}])

pub_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24')
pub_subnet = pub_response['Subnet']['SubnetId']
ec2.create_tags(Resources=[pub_subnet], Tags=[{'Key': 'Name', 'Value': 'PublicSubnet'}])

priv_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24')
priv_subnet = priv_response['Subnet']['SubnetId']
ec2.create_tags(Resources=[priv_subnet], Tags=[{'Key': 'Name', 'Value': 'PrivateSubnet'}])
