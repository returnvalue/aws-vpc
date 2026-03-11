resource "aws_vpc" "production" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "ProductionVPC" }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.production.id
  cidr_block        = "10.0.1.0/24"
  tags = { Name = "PublicSubnet" }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.production.id
  cidr_block        = "10.0.2.0/24"
  tags = { Name = "PrivateSubnet" }
}
