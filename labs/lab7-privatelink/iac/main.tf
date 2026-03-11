resource "aws_lb" "privatelink_nlb" {
  name               = "PrivateLinkNLB"
  internal           = true
  load_balancer_type = "network"
  subnets            = [var.prod_priv_subnet_id]
}

resource "aws_vpc_endpoint_service" "provider" {
  acceptance_required        = true
  network_load_balancer_arns = [aws_lb.privatelink_nlb.arn]
}

resource "aws_vpc_endpoint" "consumer" {
  vpc_id            = var.analytics_vpc_id
  service_name      = aws_vpc_endpoint_service.provider.service_name
  vpc_endpoint_type = "Interface"
  subnet_ids        = [var.analytics_subnet_id]
}
