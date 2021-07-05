# kmwdpoh-162738

This section contains the AWS CDK code written in Typescript. 

For more information about CDK, please see the [CDK prerequisites](https://docs.aws.amazon.com/cdk/latest/guide/work-with.html#work-with-prerequisites)

For more information on using the CDK in Typescript, please see the [Developer Guide](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-typescript.html). 



How to find out EC2 AMI id of the 1-click node

![ami-id](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-ami-id.jpg)



## Key Objectives of the code

1. provision an EC2 instance of *Crypto.org Chain 1-Click Node*
2. SSH into the EC2 and start the test net



## Caution:

  make sure in your AWS account there is no overlap with this Vpc cidr 10.1.2.0/24

## Key implementations:

Vpc & subnets

```typescript
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
```

Ec2

```typescript
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
```

Security group rules

```typescript
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
```



## Run the cdk code

To run a CDK Typescript, execute the following:

```bash
$ git clone git@github.com:ShengzhenFu/kmwdpoh-162738.git
$ cd kmwdpoh-162738/ec2
$ npm install -g aws-cdk
$ npm install
$ cdk deploy
```

You will be able to see below prompt, proceed with Y

![cdk deploy](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-deploy.png)

And after a few minutes you will be able to see the result of an Public IP address of the ec2

![output](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-deployed.jpg)

EC2 created along with subnets 

![subnets](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-subnets.jpg)

security group rules

![security group rules](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-sg.jpg)

## Start testnet

```bash
ssh -i crypto-instance-key.pem ubuntu@IP
```

```bash
$ sudo -u crypto /chain/reconfig.sh
Please select either mainnet(M) or testnet(T) to join (M/T): M
You can select the following networks to join
	0. crypto-org-chain-mainnet-1
Please choose the network to join by index (0/1/...): 0
The selected network is crypto-org-chain-mainnet-1
The genesis does not exit or the sha256sum does not match the target one. Download the target genesis from github.
💾 Downloading crypto-org-chain-mainnet-1 genesis
```

And follow the steps of how to run testnet , you will be able to get testnet up like i did below

![testnet up](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-testNet-started.jpg)



## To dispose of the stack/s afterwards

```bash
$ cdk destroy
## this will remove all the resources has been created above like ec2, subnets, security groups, etc
```

resource destroyed

![cdk destroy](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-destroy.jpg)





Any questions or issue when run the code, feel free to create issue in the repo,

or contact me at fushengzhen@163.com
