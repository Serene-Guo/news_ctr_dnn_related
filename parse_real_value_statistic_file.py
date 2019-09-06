import json

import os

feature_dict = {}


f_meta = open("meta.conf", "r")
for line in f_meta:
    line = line.strip()
    line_arr = line.split("\t")
    if len(line_arr) < 4:
        continue
    fid = line_arr[0]
    pb_type = line_arr[1]
    fname = line_arr[3]

    is_continuous =(fid in ['3273']) or (pb_type in ['double']) or (fname in ['d_cont_char_count', 'd_v_play_length'])
     
    feature_dict[fid] = [fname, is_continuous]

#print (len(feature_dict))
f_meta.close()
    

## 2045_CDF    user_recoms_log {'v1': [0.02], 'v2':[..., .., .., ]}

f_statistic = open("./c-1-s001-2019-09-03.json/part-00000", "r")

for line in f_statistic:
    line = line.strip()
    statistic_dict = json.loads(line)
f_statistic.close()

out_list = []
has_fid_set = set()
for key in statistic_dict:
    
    key_arr = key.split("_")
    fea_id = key_arr[0]

    if fea_id not in feature_dict:
        continue
    fea_name = feature_dict[fea_id][0]
    has_fid_set.add(fea_id)

    if "CDF" in key or "WordCount" in key:
        value = statistic_dict[key]
        if "v1" not in value or "v2" not in value:
            print ("not find v1, or v2")
            continue
        v1_key_list = value["v1"]
        v2_value_list = value["v2"]
        statistic_dict[key]["v1"] = v1_key_list[:10]
        statistic_dict[key]["v2"] = v2_value_list[:10]
    fea_tuple = (key, fea_name, statistic_dict[key])
    out_list.append(fea_tuple)


a = sorted(out_list, key= lambda x:x[0])

for i in a:
    print ("\t".join([str(x) for x in i]))


for i in feature_dict:
    if i not in has_fid_set:
        name = feature_dict[i][0]
        if feature_dict[i][1]:
            print ("%s\t%s\tnot in feature_statistic_file" % (i, name))
