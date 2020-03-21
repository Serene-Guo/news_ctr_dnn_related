import os

train_data_txt = "./x"

f_in = open(train_data_txt)
for line in f_in:
    line = line.strip()
    line_arr = line.split("\t")
    if len(line_arr) != 6:
        continue
    
    ## sample_num, label, ?, continous_fea, discrete_fea, fixedsize fea.

    fixsize = line_arr[5]
    feas = fixsize.split(",")
    for fea in feas:
        fea_num = fea.split()
        print (str(len(fea_num)) + "\t" + fea)
