import os
import json

feature_conf_file = "feature_confs/2020-03-23_feature_conf.json"
feature_conf_file = 'feature_confs/old_frame_new_data_0309_feature_conf.json'
feature_conf_file = 'feature_confs/gff_v0_0327_feature_conf.json'
feature_conf_file = 'feature_confs/recml_clkhis_feature_conf.json'
feature_conf_file = 'feature_confs/feature_conf_no_3073.json'
fea_name = 'feature_conf_0.json'
fea_name = '0309_sample_feature_conf.json'

fea_name = 'feature_conf_2.json'
fea_name = 'old_frame_feature_conf.json'
feature_conf_file = 'feature_confs/' + fea_name

f_in = open(feature_conf_file, "r")

json_dict = json.load(f_in)

#print (len(json_dict))

discrete_fea_list = []
continous_fea_list = []
fixedsize_fea_list = []

for fea_dict in json_dict:
    if "visible" not in fea_dict:
        print (fea_dict)
        continue
    visible = fea_dict["visible"]
    if not visible:
        continue
    if "otype" not in fea_dict:
        continue
    otype = fea_dict['otype']
    desc = "desc_null"
    if "desc" in fea_dict:
        desc = fea_dict["desc"]
    output = "output_null"
    if "output" in fea_dict:
        output = fea_dict["output"]
    if otype == "Discrete":
        discrete_fea_list.append((desc, output))
    elif otype == "FixedSize":
        fixedsize_fea_list.append((desc, output))
    elif otype == "Continuous":
        continous_fea_list.append((desc, output))
    else:
        continue

out_str = ""
for fea in continous_fea_list:
    #out_str += ":".join(fea)
    #out_str += ","
    print ('\t'.join(['cont_fea', ":".join(fea)]))

#out_str = out_str.strip(",")
#out_str += "\t"

for fea in discrete_fea_list:
    #out_str += ":".join(fea)
    #out_str += ","
    print ('\t'.join(['disc_fea', ":".join(fea)]))

#out_str = out_str.strip(",")
#out_str += "\t"

for fea in fixedsize_fea_list:
    #out_str += ":".join(fea)
    #out_str += ","
    print ('\t'.join(['fixed_fea', ":".join(fea)]))

#out_str = out_str.strip(",")

#print (out_str)


