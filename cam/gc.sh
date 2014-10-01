#!/bin/sh

echo "`whoami`: gc.sh  start at `date`" >> /tmp/cron

today=`date +"%Y%m%d"`
yesterday=`date +"%Y%m%d" -d "1 day ago"`

cmd="find . | grep \".*_\(${today}\|${yesterday}\)-.*\" -v | xargs rm"
echo $cmd
eval $cmd

echo "`whoami`: gc.sh  start at `date`" >> /tmp/cron
