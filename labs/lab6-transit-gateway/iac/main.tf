resource "aws_ec2_transit_gateway" "hub" {
  description = "Central Hub"
}

resource "aws_vpc" "shared" {
  cidr_block = "10.2.0.0/16"
}

resource "aws_subnet" "shared" {
  vpc_id     = aws_vpc.shared.id
  cidr_block = "10.2.1.0/24"
}

resource "aws_ec2_transit_gateway_vpc_attachment" "prod" {
  subnet_ids         = [var.prod_priv_subnet_id]
  transit_gateway_id = aws_ec2_transit_gateway.hub.id
  vpc_id             = var.prod_vpc_id
}

resource "aws_ec2_transit_gateway_vpc_attachment" "shared" {
  subnet_ids         = [aws_subnet.shared.id]
  transit_gateway_id = aws_ec2_transit_gateway.hub.id
  vpc_id             = aws_vpc.shared.id
}
