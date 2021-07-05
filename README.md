# kmwdpoh-162738

This section contains the AWS CDK code written in Typescript. For more information on using the CDK in Typescript, please see the [Developer Guide](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-typescript.html).



How to find out EC2 AMI id of the 1-click node

![ami-id](https://github.com/ShengzhenFu/kmwdpoh-162738/raw/main/images/ec2-ami-id.jpg)



## Key Objectives of the code

1. provision an EC2 instance of *Crypto.org Chain 1-Click Node*
2. SSH into the EC2 and start the test net

## Provision EC2

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

