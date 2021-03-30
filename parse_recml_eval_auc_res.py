import sys
#f_base = "./eval_auc/base_auc"
f_base = sys.argv[1]

print (f_base)

f_in = open(f_base, "r")

one_hour_auc_start =False
model_name =None

print ("\t".join(["model_name", "data_str", "model_version","auc", "gauc", "samples_num", "user_num"]))
for line in f_in:
    line = line.strip()
    line_arr = line.split(",")
    if len(line_arr) < 3:
        continue
    if "log" in line:
        one_hour_auc_start =True
        log_name = line_arr[0]
        log_name = log_name.strip("==>").strip("<==").strip()
        log_name_arr = log_name.split("_")
        model_name = "_".join(log_name_arr[:-1])
        data_str = log_name_arr[-1][:8]
    elif "auc" in line and "gauc" not in line:
        model_version = line_arr[0].split(":")[-1].strip()
        auc = line_arr[1].split(":")[-1].strip()
        samples_num = line_arr[2].strip().split(" ")[0].strip()
    elif "gauc" in line:
        #model_version2 = line_arr[0].split(":")[-1].strip()
        gauc = line_arr[1].split(":")[-1].strip()
        user_num = line_arr[2].strip().split(" ")[0].strip()
        one_hour_auc_start =False
    else:
        continue
    

    if not one_hour_auc_start:
        if model_name is not None:
            print ("\t".join([model_name, data_str, model_version,auc, gauc, samples_num, user_num]))
        [model_name, data_str, model_version,auc, gauc, samples_num, user_num] = ["nu"] * 7

