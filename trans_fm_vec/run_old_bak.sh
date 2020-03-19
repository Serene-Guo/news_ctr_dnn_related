#!/bin/bash
source ~/jiande/.bashrc

export HOME=/home/appops
export HADOOP_HOME=${HOME}/jiande/hadoop-2.7.3
export JAVA_HOME=${HOME}/jiande/jdk1.8.0_171
export JRE_HOME=$JAVA_HOME/jre
export SPARK_HOME=${HOME}/jiande/spark-2.1.1-bin-hadoop2.7.3
hadoop=${HADOOP_HOME}/bin/hadoop
function wait_input()
{
  wait_counts=$1 
  check_path1=$2
  wait_interval=$[6*60] #sec  6min
  for (( i=0;i< $wait_counts;i++ ))
  do
    ${HADOOP_HOME}/bin/hadoop fs -test -e  $check_path1
    if [[ $? -eq 0 ]] ;then
      echo "ok the file exist"
      break
    fi
    sleep $wait_interval
    echo "($i) the file is not ok--- " $check_path1
  done
  ${HADOOP_HOME}/bin/hadoop fs -test -e  $check_path1
}
#--------------------------------------------------------------------
##  hdfs://hz-cluster9/
day=$(date -d -1day +%Y%m%d)
fm_raw="/user/datacenter/recall/fm/model_all_64/$day"
hdfs_vec="/user/datacenter/mlp/deep/fm_vec/$day"

wait_input 10 $fm_raw/model.$day

$hadoop fs -get $fm_raw

output='./output'

rm -r $output && mkdir -p $output

for filename in $(ls $day)
do
  cat ${day}/$filename | python trans_new.py $output $filename &
done

wait

cat $output/doc/* > doc
cat $output/user/* > user

$hadoop fs -mkdir -p $hdfs_vec 
$hadoop fs -rm $hdfs_vec/*
$hadoop fs -put doc user $hdfs_vec/

echo "rm local data. 1 day ago"
day4=`date +%Y%m%d -d "1 day ago"`
rm -r $day4

echo "hadoop fs -rm /user/datacenter/mlp/deep/fm_vec/  14 day ago."
day14=`date +%Y%m%d -d "14 day ago"`
#$hadoop fs -rmr "/user/datacenter/mlp/deep/fm_vec/${day14}"


echo 'all done.'
