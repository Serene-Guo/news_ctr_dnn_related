#!/bin/bash

date_str=`date -d "1 hour ago" +%Y-%m-%d`
tmp_hour_str=`date -d "1 hour ago" +%H`
hour_str=$(echo -e $tmp_hour_str | sed -r 's/0*([0-9])/\1/')

echo ${date_str}
echo ${hour_str}

upload_path=$1
branch=$2

if [ ${upload_path}x == "x" -o ${branch}x == "x" ];then
    echo "need 2 param, upload_path/branch param"
    exit 1
fi

cmd="python3 hz_gen_sample.py --upload_path=${upload_path} --output_partition=203 --sample_date=${date_str} --sample_time=${hour_str}"

echo "${cmd}"

dir_path="/home/recsys/guofangfang/dlp_qingzhou/gen_sample_ini_files/"
source_file_name="${dir_path}/hourly_gen_sample.ini"
target_file_name="${dir_path}/${upload_path}_${date_str}-${tmp_hour_str}_hourly_gen_sample.ini"

python rewrite_dlp_job_file.py \
    --source_file_name="${source_file_name}" \
    --new_cmd="${cmd}" \
    --new_branch="${branch}" \
    --target_file_name="${target_file_name}"

