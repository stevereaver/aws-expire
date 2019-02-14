#!/usr/bin/bash
#
# --------------------------------------------------------------------------
# Name:         zfs cron
# By:           Stephen Bancroft
# Date:         13/02/19
#
# Desc:         This script is called from zabbix's cron and is used to 
#               collect the state of the AWS instance
#
# Usage:        aws_cron.sh
# --------------------------------------------------------------------------
#

RESINST=~scripts/aws/describe_reserved_instances.py
SENDER=/usr/bin/zabbix_sender
ZABBIX=zabbix.local
PORT=10050

$RESINST --profile itg | $SENDER -i - -z $ZABBIX -p $PORT > /dev/null 2>&1
$RESINST --profile sws | $SENDER -i - -z $ZABBIX -p $PORT > /dev/null 2>&1
