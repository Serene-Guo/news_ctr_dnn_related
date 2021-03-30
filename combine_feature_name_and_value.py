
f_name = "./feature_confs/feature_name.txt"

f_value = "../train_data_nan_value/2020-02-17-17--nan"


f_in1 = open(f_name, 'r')

conti_fea = []
dis_fea = []
fixed_fea = []

for line in f_in1:
    line = line.strip()
    line_arr = line.split('\t')
    ##  0: continouts 1: discrete 2: fixed_size fea
    conti_fea = line_arr[0].strip(',').split(',')
    dis_fea = line_arr[1].strip(',').split(',')
    fixed_fea = line_arr[2].strip(',').split(',')
