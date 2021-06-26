from aws_cdk import aws_ec2 as ec2, core


class vpcStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Vpc, subnets provision
        self.vpc = ec2.Vpc(
            self,
            "vpc-crypto",
            cidr="10.1.2.1/24",  # vpc cidr ip range
            max_azs=2,  # multiple AZ for redundant
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-subnet-crypto",
                    subnet_type=ec2.SubnetType.PUBLIC,  # public subnet
                    cidr_mask=26,
                ),
                ec2.SubnetConfiguration(
                    name="private-subnet-crypto",
                    subnet_type=ec2.SubnetType.PRIVATE,  # private subnet
                    cidr_mask=26,
                ),
            ],
            nat_gateways=1,  # share 1 nat gw
        )
