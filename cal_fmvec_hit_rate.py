fmvec_file = "./fmvec_tmp/cat.txt"
fmvec_file = "./fmvec_tmp/poi.txt"
fmvec_file = "./fmvec_tmp/keyword.txt"

f_statistic = "./fmvec_tmp/recent_tag_in_statistic"

f_fm = open(fmvec_file)
poi_set = set()

for line in f_fm:
    line = line.strip()
    line_arr = line.split()
    if len(line_arr) != 65:
        print (line)
        continue
    poi_set.add(line_arr[0])

f_fm.close()



f_stat = open(f_statistic)
for line in f_stat:
    line = line.strip()
    line_arr = line.split("\t")
    if len(line_arr) != 2:
        print (line)
    poi = line_arr[0]
    if poi not in poi_set:
        print (poi + "\t not in fmvec_table!")
f_stat.close()


