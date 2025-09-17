data "aws_subnets" "by_cidr_az" {
  filter {
    name   = "cidr-block"
    values = ["172.31.96.0/20"]
  }
  filter {
    name   = "availability-zone"
    values = ["ap-southeast-2a"]
  }
}

# Resolve attributes for the first (expected only) match
data "aws_subnet" "target" {
  id = data.aws_subnets.by_cidr_az.ids[0]
}

# Reuse the default security group in that VPC
data "aws_security_group" "default_in_vpc" {
  name   = "default"
  vpc_id = data.aws_subnet.target.vpc_id
}