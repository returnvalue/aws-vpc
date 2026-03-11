resource "aws_security_group" "web" {
  name        = "WebServerSG"
  description = "Allow HTTP"
  vpc_id      = var.vpc_id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_network_acl" "public" {
  vpc_id = var.vpc_id
  subnet_ids = [var.public_subnet_id]
}

resource "aws_network_acl_rule" "deny_malicious" {
  network_acl_id = aws_network_acl.public.id
  rule_number    = 100
  egress         = false
  protocol       = "-1"
  rule_action    = "deny"
  cidr_block     = "203.0.113.50/32"
}

resource "aws_network_acl_rule" "allow_all" {
  network_acl_id = aws_network_acl.public.id
  rule_number    = 200
  egress         = false
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
}
