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

#for i in feature_dict:
#    print ("%s\t%s\t%d" % (i, feature_dict[i][0], feature_dict[i][1]))

#os.sys.exit(0)

#print (len(feature_dict))
f_meta.close()
    

## 2045_CDF    user_recoms_log {'v1': [0.02], 'v2':[..., .., .., ]}

f_statistic = open("./m-2c-d-2020-03-09.json", "r")

statistic_dict = json.load(f_statistic)
test_fea_list = ['2084', '2085', '2088', '2089']
test_fea_list = ['3287', '3289', '3291', '3293']
test_fea_list = ['3273']

out_list = []
has_fid_set = set()
for key in statistic_dict:
    
    key_arr = key.split("_")
    fea_id = key_arr[0]
    fea_id = fea_id.split("-")[0]
    if fea_id not in  test_fea_list:
        continue
    fea_len = 0
    if fea_id not in feature_dict:
        continue
    fea_name = feature_dict[fea_id][0]
    has_fid_set.add(fea_id)

    if "CDF" in key or "WordCount" in key:
        value = statistic_dict[key]
        if "v1" not in value or "v2" not in value:
            print ("not find v1, or v2")
            continue
        if "WordCount" in key:
            fea_len = len(value["v1"])
        v1_key_list = value["v1"]
        v2_value_list = value["v2"]
        #statistic_dict[key]["v1"] = v1_key_list[:10]
        #statistic_dict[key]["v2"] = v2_value_list[:10]
        for i in range(len(v1_key_list)):
            print ('\t'.join([key_arr[0], fea_name, str(fea_len), str(v1_key_list[i]), str(v2_value_list[i])]))
    fea_tuple = (key, fea_name, fea_len, statistic_dict[key])
    out_list.append(fea_tuple)


#a = sorted(out_list, key= lambda x:x[0])

#for i in a:
#    print ("\t".join([str(x) for x in i]))


#for i in feature_dict:
#    if i not in has_fid_set:
#        name = feature_dict[i][0]
#        print ("%s\t%s\tnot in feature_statistic_file" % (i, name))
