
if [ $# != 2 ];then
    echo "need 2 param: upload_path(train_data_sub_dir), and branch_name"
    exit 1
fi

upload_path=$1

branch_name=$2

if [ ${upload_path}x == "x" ];then
    echo "upload_path is null string."
    exit 1
fi

if [ ${branch_name}x == "x" ];then
    echo "branch_name is null string."
    exit 1
fi


echo "done."

cd /home/recsys/guofangfang/dnn_ctr_relate/news_ctr_dnn_related 

bash ./rewrite_dlp_job_file.sh "${upload_path}"  "${branch_name}" 1>${upload_path}_rewrite.log 2>&1


### start submit job to dlp
export PATH="/home/recsys/platform/anaconda3/bin:$PATH"
cd /home/recsys/guofangfang/dlp

./dlp create -f ./gen_sample_ini_files/${upload_path}_$(date -d "1 hour ago" +\%Y-\%m-\%d-\%H)_hourly_gen_sample.ini 1>./samp_log/${upload_path}_$(date -d "1 hour ago" +\%Y-\%m-\%d-\%H-\%M)_gen_sample.log 2>&1
