import * as cdk from '@aws-cdk/core';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as iam from '@aws-cdk/aws-iam';
import { SubnetType } from '@aws-cdk/aws-ec2';



export class Ec2Stack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const cryptoVpc = new ec2.Vpc(this, 'vpc-crypto',{
      cidr: "10.1.2.0/24",
      maxAzs: 1,  // suggest >=2 for AZ redundant
      enableDnsHostnames: true,
      enableDnsSupport: true,
      natGateways: 1,
      subnetConfiguration: [
        {
          name: "public-subnet",  // public subnet
          cidrMask: 26,
          subnetType: SubnetType.PUBLIC,
        },
        {
          name: "private-subnet",  // private subnet
          cidrMask: 26,
          subnetType: SubnetType.PRIVATE,
        }
      ]
    })

    // assume role for the instance
    const role = new iam.Role(
      this,
      'crypto-instance-1-role', // this is a unique id that will represent this resource in a Cloudformation template
      { assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com') }
    )

  // lets create a security group for our instance
  // A security group acts as a virtual firewall for your instance to control inbound and outbound traffic.
  const securityGroup = new ec2.SecurityGroup(
    this,
    'crypto-instance-1-sg',
    {
      vpc: cryptoVpc,
      allowAllOutbound: true, // will let your instance send outboud traffic
      securityGroupName: 'crypto-instance-1-sg',
    }
  )

  // setup security group to allow inbound traffic on specific ports
  securityGroup.addIngressRule(
    ec2.Peer.anyIpv4(),
    ec2.Port.tcp(22),
    'Allows SSH access from Internet'
  )

  securityGroup.addIngressRule(
    ec2.Peer.anyIpv4(),
    ec2.Port.tcp(26656),
    'Allows port 26656 access from Internet'
  )

  securityGroup.addIngressRule(
    ec2.Peer.anyIpv4(),
    ec2.Port.tcp(26657),
    'Allows port 26657 access from Internet'
  )

  securityGroup.addIngressRule(
    ec2.Peer.anyIpv4(),
    ec2.Port.tcp(1317),
    'Allows port 1317 access from Internet'
  )

  

  // provisions ec2 instance
  const instance = new ec2.Instance(this, 'crypto-instance-1', {
    vpc: cryptoVpc,
    role: role,
    securityGroup: securityGroup,
    instanceName: 'crypto-instance-1',
    instanceType: ec2.InstanceType.of( // t2.micro has free tier usage in aws
      ec2.InstanceClass.T2,
      ec2.InstanceSize.MICRO
    ),
    machineImage: ec2.MachineImage.genericLinux({
      'us-west-2': 'ami-0a6250f2d58bf49ba',
      'us-east-1': 'ami-0a1e6e1045672988e'
    }) ,
    vpcSubnets: {subnetType: ec2.SubnetType.PUBLIC},
    keyName: 'crypto-instance-key', // we will create this in the console before we deploy
  })

  // cdk lets us output prperties of the resources we create after they are created
  // we want the ip address of this new instance so we can ssh into it later
  new cdk.CfnOutput(this, 'simple-instance-1-output', {
    value: instance.instancePublicIp
  })
  }
}
