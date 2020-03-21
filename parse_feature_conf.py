import os
import json

feature_conf_file = "2020-02-20_v8_feature_conf.json"

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
    out_str += ":".join(fea)
    out_str += ","

out_str = out_str.strip(",")
out_str += "\t"

for fea in discrete_fea_list:
    out_str += ":".join(fea)
    out_str += ","

out_str = out_str.strip(",")
out_str += "\t"

for fea in fixedsize_fea_list:
    out_str += ":".join(fea)
    out_str += ","

out_str = out_str.strip(",")

print (out_str)


