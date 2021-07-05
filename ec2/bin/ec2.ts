#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { Ec2Stack } from '../lib/ec2-stack';

require('dotenv').config()

const envUS = {
  env: {
    account: process.env.AWS_ACCOUNT_ID, 
    region: process.env.AWS_ACCOUNT_REGION
  }
}

const app = new cdk.App();
new Ec2Stack(app, 'Ec2Stack', {
  env: envUS.env
  });
