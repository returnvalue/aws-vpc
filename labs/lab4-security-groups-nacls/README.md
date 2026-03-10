# Lab 4: Defense in Depth (Security Groups vs. NACLs)

**Goal:** Implement stateful Security Groups that automatically allow return traffic, and stateless Network ACLs with explicit Deny rules.

```bash
# 1. Security Group (Stateful - allow HTTP inbound)
SG_ID=$(awslocal ec2 create-security-group --group-name WebServerSG --description "Allow HTTP" --vpc-id $VPC_ID --query 'GroupId' --output text)
awslocal ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0

# 2. Network ACL (Stateless - Explicit Deny of a specific IP at the subnet boundary)
NACL_ID=$(awslocal ec2 create-network-acl --vpc-id $VPC_ID --query 'NetworkAcl.NetworkAclId' --output text)

# Deny malicious IP (Rule 100)
awslocal ec2 create-network-acl-entry --network-acl-id $NACL_ID --ingress --rule-number 100 --protocol -1 --cidr-block 203.0.113.50/32 --rule-action deny

# Allow all other traffic (Rule 200)
awslocal ec2 create-network-acl-entry --network-acl-id $NACL_ID --ingress --rule-number 200 --protocol -1 --cidr-block 0.0.0.0/0 --rule-action allow

# Associate NACL with Public Subnet
awslocal ec2 replace-network-acl-association \
  --association-id $(awslocal ec2 describe-network-acls --filters Name=vpc-id,Values=$VPC_ID --query 'NetworkAcls[0].Associations[0].NetworkAclAssociationId' --output text) \
  --network-acl-id $NACL_ID
```
