
train_data_dir="hdfs://hz-cluster9/user/portal/ODM/RECOMMEND/recsys2_pctr/toutiao/txt/hourly/clean/new_feature_utid_model"

hadoop_bin="/home/recsys/platform/hadoop-jd-2.7.3/bin/hadoop"

target_dir="hdfs://hz-cluster9/user/portal/ODM/RECOMMEND/recsys2_pctr/toutiao/txt/guofangfang/test_gauc_new_feature_utid_model/"


date_time=`date -d ""`

date_str="2019-09-08"

while [ $date_str != "2019-09-09" ]
do
    echo "start copy ${date_str}"
    ${hadoop_bin} fs -mkdir ${target_dir}/${date_str}
    i=0
    while [  $i  -le  23  ]
    do
        echo "start copy ${date_str}/$i"
        cmd="${hadoop_bin} fs -cp ${train_data_dir}/${date_str}/${i} ${target_dir}/${date_str}"
        echo ${cmd}
        `$cmd`
        let i++
    done

    date_str=`date -d ${date_str}"+1 day" +"%Y-%m-%d"`
done






