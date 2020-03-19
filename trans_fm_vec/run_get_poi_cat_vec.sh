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
#fm_raw="/user/datacenter/recall/fm/model_all_64/$day"
fm_raw="/user/datacenter/recall/mf_recall/model_data/$day"
## poi/tag/cat fm_raw="/user/datacenter/recall/fm_feature/model_data/$day"
### output 
hdfs_vec="/user/datacenter/mlp/deep/fm_vec/$day"
fmvec_binary_2="/user/portal/ODM/RECOMMEND/recsys2_pctr/toutiao/fmvec_binary/$day"

###  poi/cat/tag/sourcename
#fm_raw="/user/datacenter/recall/fm_feature/model_data/$day"
###output_dir
#hdfs_vec="/user/datacenter/mlp/deep/fm_vec/$day"
#fmvec_binary_2="/user/portal/ODM/RECOMMEND/recsys2_pctr/toutiao/fmvec_binary/$day"

tmp_output_dir=${day}"_output"
mkdir ${tmp_output_dir}

output='./output'
rm -r $output && mkdir -p $output


###################
wait_input 10 $fm_raw/model.$day

rm -r ${day}
$hadoop fs -get $fm_raw

#devid_file="./devid_data/devid_2019-11-19.txt"
devid_file="./devid_data/devid_2019-12-26.txt"

for filename in $(ls $day)
do
  cat ${day}/$filename | python trans_new.py $output $filename $devid_file &
done

wait


rm ${tmp_output_dir}/doc
rm ${tmp_output_dir}/user

cat $output/doc/* > ${tmp_output_dir}/doc
cat $output/user/* > ${tmp_output_dir}/user

$hadoop fs -mkdir -p $hdfs_vec 
$hadoop fs -rm $hdfs_vec/*
$hadoop fs -put ${tmp_output_dir}/doc ${tmp_output_dir}/user $hdfs_vec/

#fmvec_binary_2
$hadoop fs -mkdir -p $fmvec_binary_2
$hadoop fs -rm $fmvec_binary_2/*
$hadoop fs -put ${tmp_output_dir}/doc ${tmp_output_dir}/user $fmvec_binary_2/

echo "rm local data. 1 day ago"
day4=`date +%Y%m%d -d "1 day ago"`
rm -r $day4

#echo "hadoop fs -rm /user/datacenter/mlp/deep/fm_vec/  14 day ago."
#day14=`date +%Y%m%d -d "14 day ago"`
#$hadoop fs -rmr "/user/datacenter/mlp/deep/fm_vec/${day14}"



echo "generate devid/docid embedding vec Done."
echo "..."
echo "..."
echo "..."

########################
echo "start get cat/poi/source_name/keyword embedding."

## another hdfs dir
###  poi/tag/cat fm vec
fm_raw="/user/datacenter/recall/fm_feature/model_data/$day"
###output_dir
hdfs_vec="/user/datacenter/mlp/deep/fm_vec/$day"
fmvec_binary_2="/user/portal/ODM/RECOMMEND/recsys2_pctr/toutiao/fmvec_binary/$day"

wait_input 10 $fm_raw/model.$day

rm -r ${day}
$hadoop fs -get $fm_raw


for filename in $(ls $day)
do
  ### do not dedup between different input files.
  cat ${day}/$filename | python trans_poi.py $output $filename &
done

wait

rm ${tmp_output_dir}/cat
rm ${tmp_output_dir}/poi
rm ${tmp_output_dir}/keyword
rm ${tmp_output_dir}/source_name

cat $output/cat/* > ${tmp_output_dir}/cat
cat $output/poi/* > ${tmp_output_dir}/poi
cat $output/keyword/* > ${tmp_output_dir}/keyword
cat $output/source_name/* > ${tmp_output_dir}/source_name

#$hadoop fs -mkdir -p $hdfs_vec 
#$hadoop fs -rm $hdfs_vec/cat
#$hadoop fs -rm $hdfs_vec/poi
#$hadoop fs -rm $hdfs_vec/keyword
#$hadoop fs -rm $hdfs_vec/source_name

$hadoop fs -put ${tmp_output_dir}/cat ${tmp_output_dir}/poi ${tmp_output_dir}/keyword ${tmp_output_dir}/source_name  $hdfs_vec/


#fmvec_binary_2
$hadoop fs -put ${tmp_output_dir}/cat ${tmp_output_dir}/poi ${tmp_output_dir}/keyword ${tmp_output_dir}/source_name  $fmvec_binary_2/


echo "rm local data. 1 day ago"
day4=`date +%Y%m%d -d "1 day ago"`

rm -r $day4

day4=`date +%Y%m%d -d "4 day ago"`
tmp_output_dir=${day4}"_output"
rm -r ${tmp_output_dir}

echo "generate cat/poi/source_name/keyword embedding vec Done."

echo 'all done.'
