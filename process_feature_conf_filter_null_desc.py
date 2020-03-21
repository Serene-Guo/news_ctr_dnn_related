import os

import json

f_fea_in = "./feature_confs/feature_conf.dc-20-adam.json"
f_out_name = "./feature_confs/wjh_feature_clean.json"



#f_fea_in = "./feature_confs/feature_conf_gff.json"
#f_out_name = "./feature_confs/gff_feature_clean.json"

#f_fea_in = "./feature_confs/v8_feature_conf.json"
#f_out_name = "./feature_confs/v8_feature_clean.json"



f_in = open(f_fea_in, "r")
f_out = open(f_out_name, "w", encoding='utf-8')
fea_list = json.load(f_in)

new_list = []

print ("fea_num:" + str(len(fea_list)))
i = 0
j = 0
for fea_dict in fea_list:
    visible = fea_dict["visible"]
    if "model_desc" not in fea_dict:
        continue
    input_list = fea_dict["inputs"]
    model_desc = fea_dict["model_desc"]
    if visible and len(model_desc) == 0 :
        #print (",".join(input_list) + "|" + fea_dict["desc"] + "|" + fea_dict["output"])
        j += 1
        continue
    elif "modules" in model_desc:
        module_dict = model_desc["modules"]
        if "dnn" in module_dict:
            dnn_list = module_dict["dnn"]
            if visible and len(dnn_list) == 0:
                #print ("dnn_[]" + ",".join(input_list) + "|" + fea_dict["desc"] + "|" + fea_dict["output"])
                j+=1
                continue
    i += 1
    print (",".join(input_list) + "\t" + fea_dict["desc"] + "\t" + fea_dict["output"])

    new_list.append(fea_dict)

str_out = json.dumps(new_list, default=lambda obj: obj.__dict__, sort_keys=True, indent=2, ensure_ascii=False)

f_out.write(str_out)

print ("model_desc={}, fea_num:" + str(j))
print ("fea model_desc is not null, num:" + str(i))
