import os
import json

feature_conf_file = "feature_confs/2020-03-23_feature_conf.json"

feature_conf_file = 'feature_confs/wjh_v13_feature_conf.json'

feature_conf_file = 'feature_confs/gff_v0_0327_feature_conf.json'

outfile_name = 'feature_confs/sort_gff_v0_0327_feature_conf.json'


feature_conf_file = 'feature_confs/v8_old_frame_0327_feature_conf.json'
outfile_name = 'feature_confs/sort_v8_old_frame_0327_feature_conf.json'


feature_conf_file = 'feature_confs/xjg_video_v13_feature_conf.json'
outfile_name = 'feature_confs/sort_xjg_video_v13_feature_conf.json'

f_in = open(feature_conf_file, "r")
f_out = open(outfile_name, 'w')

json_dict = json.load(f_in)

#print (len(json_dict))

discrete_fea_list = []
continous_fea_list = []
fixedsize_fea_list = []

list_of_tuple = []
for fea_dict in json_dict:
    visible = fea_dict["visible"]
    inputs = []
    if "inputs" in fea_dict:
        inputs = fea_dict["inputs"]
    
    sort_input = 0
    if len(inputs) == 0:
        print (fea_dict)
        continue
    if len(inputs) ==1:
        sort_input = inputs[0]
    else:
       ## inputs: ['2082_hash', '2084'], "inputs": ['2036_idx', '3306_idx'] 
        #inputs_new = []
        #for a_input in inputs:
        #    a_input_idx = a_input.strip().split('_')[0]
        #    inputs_new.append(a_input_idx)
        inputs.sort()
        sort_input = inputs[0]

    tuple_1 = (sort_input, fea_dict)
    list_of_tuple.append(tuple_1)

list_of_tuple.sort(key=lambda x:x[0])

new_fea_list = [x[1] for x in list_of_tuple]

#out_str = json.dumps(new_fea_list, default=lambda obj: obj.__dict__, indent=2, ensure_ascii=False)
out_str = json.dumps(new_fea_list,  indent=2, ensure_ascii=False)

f_out.write(out_str)
f_out.close()

