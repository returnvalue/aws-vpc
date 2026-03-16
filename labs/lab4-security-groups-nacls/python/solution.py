import boto3

ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

vpcs = ec2.describe_vpcs(Filters=[{'Name': 'tag:Name', 'Values': ['ProductionVPC']}])
vpc_id = vpcs['Vpcs'][0]['VpcId']

sg_response = ec2.create_security_group(
    GroupName='WebServerSG',
    Description='Allow HTTP',
    VpcId=vpc_id
)
sg_id = sg_response['GroupId']
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpProtocol='tcp',
    FromPort=80,
    ToPort=80,
    CidrIp='0.0.0.0/0'
)

nacl_response = ec2.create_network_acl(VpcId=vpc_id)
nacl_id = nacl_response['NetworkAcl']['NetworkAclId']

ec2.create_network_acl_entry(
    NetworkAclId=nacl_id,
    Ingress=True,
    RuleNumber=100,
    Protocol='-1',
    CidrBlock='203.0.113.50/32',
    RuleAction='deny'
)

ec2.create_network_acl_entry(
    NetworkAclId=nacl_id,
    Ingress=True,
    RuleNumber=200,
    Protocol='-1',
    CidrBlock='0.0.0.0/0',
    RuleAction='allow'
)

assoc_response = ec2.describe_network_acls(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
assoc_id = assoc_response['NetworkAcls'][0]['Associations'][0]['NetworkAclAssociationId']

ec2.replace_network_acl_association(
    AssociationId=assoc_id,
    NetworkAclId=nacl_id
)
