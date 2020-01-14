import os
from os import listdir
import json

input_dir = "./13/"
files = listdir(input_dir)

for file_name in files:
    f_in = open(input_dir + file_name)
    for line in f_in:
        line = line.strip()
        json_dict = json.loads(line)
        
        [id_, label, score, model, is_ctr_rec, user, devid] = ["NULL"] * 7

        user = "NULL"
        devid = "NULL"
        
        if "urs" in json_dict:
            user = json_dict["urs"]
        if "devId" in json_dict:
            devid = json_dict["devId"]
        
        id_ = devid
        if "modelName" in json_dict:
            model = json_dict["modelName"]

        if "doc" in json_dict:
            doc_dict = json_dict["doc"]
            for docid in doc_dict:
                [label, score, is_ctr_rec] = ["NULL"] * 3
                doc_info_dict = doc_dict[docid]
                if "clickLabel" in doc_info_dict:
                    label = str(doc_info_dict["clickLabel"])
                if "isCtrRec" in doc_info_dict:
                    is_ctr_rec = "1" if doc_info_dict["isCtrRec"] else "0"
                if "ctrScore" in doc_info_dict:
                    score_f = doc_info_dict["ctrScore"]
                    try:
                        score_f = float("%.5f" % score_f)
                        score = str(score_f)
                    except Exception as e:
                        pass
                print ("\t".join([id_, label, score, model, is_ctr_rec, user, devid]))
