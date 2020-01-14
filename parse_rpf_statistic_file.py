import json
import sys

#f_in = open("P_DURATION")
i = 0

docid_dict = {}
for line in sys.stdin:
    i += 1
    if i < 1:
        continue
    line = line.strip()
    line_arr = line.split("\t")
    json_str = line_arr[1]
    
    fea_name = line_arr[0]
    if fea_name != "doc_id":
        continue

    json_dict = json.loads(json_str)

    for key in json_dict:
        #print (key + "\t" + str(json_dict[key]))
        if key != "keyWCnt":
            continue
        docid_num_str = json_dict[key]
        docid_num = json.loads(docid_num_str)


        for docid in docid_num:
            if docid not in docid_dict:
                docid_dict[docid] = 0
            docid_dict[docid] += docid_num[docid]


for key in docid_dict:
    print (key + "\t" + str(docid_dict[key]))
