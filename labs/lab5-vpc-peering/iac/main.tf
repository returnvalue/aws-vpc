resource "aws_vpc" "analytics" {
  cidr_block = "10.1.0.0/16"
}

resource "aws_vpc_peering_connection" "peer" {
  vpc_id      = var.prod_vpc_id
  peer_vpc_id = aws_vpc.analytics.id
  auto_accept = true
}

resource "aws_route" "to_analytics" {
  route_table_id            = var.prod_priv_rt_id
  destination_cidr_block    = "10.1.0.0/16"
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}
