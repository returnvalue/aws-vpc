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

## 🧠 Key Concepts & Importance

- **Stateful Security Groups (SG):** Act at the **instance level**. If you allow inbound traffic on port 80, the return traffic is automatically allowed—even without an outbound rule. They are your primary line of defense.
- **Stateless Network ACLs (NACL):** Act at the **subnet boundary**. They evaluate traffic coming into and leaving the subnet. Because they are stateless, you must explicitly allow both inbound and outbound traffic.
- **Explicit Deny:** Security Groups only support "Allow" rules (everything else is denied by default). NACLs support **Deny rules**, making them ideal for blocking specific malicious IP addresses at the perimeter before they even reach your instances.
- **Order Matters:** NACL rules are evaluated in numerical order (lowest to highest). Once a match is found, processing stops.

## 🛠️ Command Reference

- `ec2 create-security-group`: Creates a security group.
- `ec2 authorize-security-group-ingress`: Adds an inbound rule to a security group.
- `ec2 create-network-acl`: Creates a network ACL.
- `ec2 create-network-acl-entry`: Creates an entry (rule) in a network ACL.
    - `--network-acl-id`: The ID of the NACL.
    - `--ingress`: Indicates the rule is for inbound traffic.
    - `--rule-number`: The rule number (order of evaluation).
    - `--protocol`: The protocol for the rule (e.g., `-1` for all).
    - `--cidr-block`: The IP range for the rule.
    - `--rule-action`: The action for the rule (`allow` or `deny`).
- `ec2 replace-network-acl-association`: Replaces the NACL associated with a subnet.
    - `--association-id`: The ID of the current association.
    - `--network-acl-id`: The ID of the new NACL to associate.
- `ec2 describe-network-acls`: Describes network ACLs, used here to find an association ID.
