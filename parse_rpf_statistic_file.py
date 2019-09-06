import json

f_in = open("P_DURATION")
i = 0
for line in f_in:
    i += 1
    if i < 1:
        continue
    line = line.strip()
    line_arr = line.split("\t")
    json_str = line_arr[1]

    json_dict = json.loads(json_str)

    for key in json_dict:
        print (key + "\t" + str(json_dict[key]))
