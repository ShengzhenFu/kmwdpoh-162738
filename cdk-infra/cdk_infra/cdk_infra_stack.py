from aws_cdk import core as cdk

from aws_cdk import (
    aws_ec2 as ec2, 
    aws_ssm as ssm, 
    aws_iam as iam, 
    aws_eks as eks, 
    )


class CdkInfraStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Vpc, subnets provision
        vpc = ec2.Vpc(
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
        # create IAM role for worker groups and k8s RBAC config
        eks_role = iam.Role(
            self,
            "eksadmin",
            assumed_by=iam.ServicePrincipal(service="ec2.amazonaws.com"),
            role_name="eks-cluster-role",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    managed_policy_name="AdministratorAccess"
                )
            ],
        )
        eks_instance_profile = iam.CfnInstanceProfile(
            self,
            "eksInstanceProfile",
            roles=[eks_role.role_name],
            instance_profile_name="eks-cluster-role",
        )

        # EKS cluster provision and attach role as master_role
        cluster = eks.Cluster(
            self,
            "test-net",
            cluster_name="eks-cluster-cryptoTestNet",
            version=eks.KubernetesVersion.V1_19,
            vpc=vpc,
            vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)],
            default_capacity=0,  # don't want to use the default EKS node group, i will create node group separately below
            masters_role=eks_role,
        )

        eks_nodegroup = cluster.add_nodegroup_capacity(
            "eks-nodegroup",
            instance_types=[
                #ec2.InstanceType("t3.large"),
                ec2.InstanceType("m5.large"),
                #ec2.InstanceType("c5.large"),
            ],
            disk_size=50,
            min_size=2,
            max_size=2,
            desired_size=2,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            remote_access=eks.NodegroupRemoteAccess(ssh_key_name="ie-prod-snow-common"),
            capacity_type=eks.CapacityType.SPOT,
        )
