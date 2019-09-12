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

f_statistic = open("./m-1c-d-2019-09-04.json", "r")

statistic_dict = json.load(f_statistic)

out_list = []
has_fid_set = set()
target_feaid_list = ['3021'] ## rec reason
target_feaid_list = ['3001', '0'] ## doc type
target_feaid_list = ['3002'] ## len_title
for key in statistic_dict:
    
    key_arr = key.split("_")
    fea_id = key_arr[0]
    fea_id = fea_id.split("-")[0]
    fea_len = 0
    
    if fea_id not in feature_dict:
        continue
    
    if fea_id not in target_feaid_list:
        continue
    fea_name = feature_dict[fea_id][0]
    has_fid_set.add(fea_id)
    
    word_count_list = []
    if "CDF" in key or "WordCount" in key:
        value = statistic_dict[key]
        if "v1" not in value or "v2" not in value:
            print ("not find v1, or v2")
            continue
        if "WordCount" in key:
            fea_len = len(value["v1"])
        v1_key_list = value["v1"]
        v2_value_list = value["v2"]
        
        index_list = sorted(range(len(v2_value_list)), key=lambda k: v2_value_list[k], reverse=True)
        v1_key_list_sort = [v1_key_list[k] for k in index_list]
        v2_value_list_sort = [v2_value_list[k] for k in index_list]

        v1_key_list = v1_key_list_sort
        v2_value_list = v2_value_list_sort
        
        num = int(fea_len / 100 ) + 1
        for i in range(num):
            end_idx = min((i+1)*100, fea_len)
            tmp_dict = {}
            tmp_dict["v1"] = v1_key_list[i*100: end_idx]
            tmp_dict["v2"] = v2_value_list[i*100: end_idx]
            word_count_list.append(tmp_dict)

        #statistic_dict[key]["v1"] = v1_key_list[:300]
        #statistic_dict[key]["v2"] = v2_value_list[:300]
    for tmp_dict in word_count_list:
        fea_tuple = (key, fea_name, fea_len, tmp_dict)
        out_list.append(fea_tuple)


a = sorted(out_list, key= lambda x:x[0])

for i in a:
    print ("\t".join([str(x) for x in i]))


os.sys.exit(0)

for i in feature_dict:
    if i not in has_fid_set:
        name = feature_dict[i][0]
        print ("%s\t%s\tnot in feature_statistic_file" % (i, name))
