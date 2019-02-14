#!/usr/bin/python
# --------------------------------------------------------------------------
# Name:         describe_reserved_instances.py
# By:           Stephen Bancroft
# Email:        bancroft@tt.com.au
# Date:         13/02/19
#
# Desc:         The python will hit AWS API and check the state 
#               if our AWS instances
#
# Usage:        describe_reserved_instances.py
# --------------------------------------------------------------------------
# URL: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_reserved_instances
#------------------------------------------------------------

import boto3
import os
import json
import pprint
import sys
import argparse, textwrap
import datetime
import pytz

utc=pytz.UTC
parser = argparse.ArgumentParser()
parser.add_argument("--profile", help="profile to use", required = True)
args = parser.parse_args()
temp=vars(args)
profile=temp['profile']
os.environ['AWS_PROFILE'] = profile
os.environ['AWS_DEFAULT_REGION'] = "<region>"
client = boto3.client('ec2')

zabbix_dir="/etc/zabbix/aws"
management_host="<management host>"

# Write out the discovered instance for zabbix to pick up later 
r = open(zabbix_dir+'/aws_instance_discovery.'+profile,'w')
instance_data=[]

response = client.describe_reserved_instances()
for instance in response['ReservedInstances']:
        inst_temp = {}
        inst_temp["{#INSTANCE}"] = instance['ReservedInstancesId']
        instance_data.append(inst_temp)
        # As we loop around print out the days until expire (may as well)
        # the output of which is sent back to zabbix
        d = (instance['End'] - utc.localize(datetime.datetime.today()))
        print management_host+" aws[instance_state_"+profile+","+instance['ReservedInstancesId']+"] "+str(d.days)
data={}
data["data"]=instance_data
r.write(json.dumps(data, indent=4))
r.close()
