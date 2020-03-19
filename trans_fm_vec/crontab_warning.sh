file2=/work/ctr_framework/ctr_framework/ctr/yf/output1
if [ ! -f "/work/ctr_framework/ctr_framework/ctr/yf/output1/_SUCCESS" ];then
  echo "FM vec faild!" | mail -s "FM vec Failed" bjguofangfang@corp.netease.com
  exit 1
fi
