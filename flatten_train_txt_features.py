#f_train_txt = ""

f_value = "../train_data_nan_value/2020-02-17-17--nan"

f_value = './feature_confs/train_data_line_1.txt'

f_in = open(f_value, "r")

conti_fea = []
dis_fea = []
fixed_fea = []
for line in f_in:
    line_arr = line.strip().split('\t')
    if len(line_arr) != 6:
        continue
    conti_fea = line_arr[3].strip().split(',')
    dis_fea = line_arr[4].strip().split(',')
    fixed_fea = line_arr[5].strip().split(',')
    


for fea in conti_fea:
    if fea == '':
        fea = 'null'
    print ('\t'.join(['cont_fea', fea]))

for fea in dis_fea:
    if fea == '':
        fea = 'null'
    print ('\t'.join(['dis_fea', fea]))

for fea in fixed_fea:
    if fea == '':
        fea = 'null'
    print ('\t'.join(['fixed_fea', fea]))


