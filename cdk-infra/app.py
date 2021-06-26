#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from aws_cdk import core
from cdk_infra.cdk_infra_stack import CdkInfraStack
from cdk_infra.vpc_stack import vpcStack


app = core.App()
env_us = core.Environment(account="440900076177", region="us-west-2")
vpc_stack = vpcStack(app, "vpcStack", env=env_us)

eks_stack = CdkInfraStack(app, "CdkInfraStack", vpc=vpc_stack.vpc, env=env_us)

app.synth()
