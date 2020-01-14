import sys
### label
#0	int32		label
#3269	bool		P_IS_DISLIKE


read_time_fea = ['3246','3247','3248','3249','3250','3251','3252','3253','3254','3255','3256','3257']

## user_click_history_fea = [str(x) for x in range(2069, 2080)] + [str(x) for x in range(2082, 2090)] + ['2092', '2093']
user_click_history_docid = ['2069', '2073', '2092', '2093'] ### not in statistic file
user_click_history_liguang = [str(x) for x in range(2082, 2090)] ## not in statistic file
user_click_history_fea = ['2070', '2071', '2072'] + [str(x) for x in range(2074, 2080)]

session_neg_gff = ['2080', '2081']
session_recent_neg_poi_tag_wd = ['2102', '2103', '3286', '3287', '3288', '3289', '3290', '3291', '3292', '3293']


user_login_fea = ['2090', '2091', '2094', '2095']
time_stamp = ['2096']

#doc_hourly_ctr_fea = [str(x) for x in range(3258, 3274)]
doc_hourly_ctr_fea = [str(x) for x in range(3258, 3268)] ## do not contain 3268
cat_timeliness_fea = ['3268']
#p_label = ['3269', '3270', '3271', '3272', '3273']


listpage_time_fea = ['2097', '2098', '2099', '2100'] + [str(x) for x in range(3274, 3286)]
third_party_label = ['2101']
tid_model_fea = ['2104','3294']
user_gentie_fea = ['2105', '2106', '2107', '2108', '2109', '2110']
doc_movie_actor_fea = ['3295', '3296', '3297', '3298', '3299', '3300']

filter_fid_list = read_time_fea + user_click_history_docid + user_click_history_liguang + user_click_history_fea + session_neg_gff + session_recent_neg_poi_tag_wd + user_login_fea + doc_hourly_ctr_fea + cat_timeliness_fea + listpage_time_fea + third_party_label + tid_model_fea + user_gentie_fea + doc_movie_actor_fea


new_fea_list = [int(x) for x in filter_fid_list]

new_fea_list_sort = sorted(new_fea_list)



#for i in new_fea_list_sort:
#    print (i)

#sys.exit(0)

#f_in = open("meta_cl.conf")
f_in = open("gff_min_fea.conf")





fea_num=0
fea_desc_dict = {}
fea_list_dict = {}
for line in f_in:
    line = line.strip()
    if len(line) < 1:
        continue
    if "###" in line:
        fea_num +=1
        fea_desc_dict[fea_num] = line
        continue
    line_arr = line.split("\t")
    if len(line_arr) < 4:
        continue
    fea_id = int(line_arr[0])

    if fea_num not in fea_list_dict:
        fea_list_dict[fea_num] = []
    #if fea_id not in new_fea_list_sort:
    fea_list_dict[fea_num].append(fea_id)
    
f_in.close()

all_fea = []
for key in fea_desc_dict:
    print (fea_desc_dict[key])
    variable_name = "fea_name_" + str(key)
    fea_list = fea_list_dict[key]
    all_fea += fea_list
    fea_list_sort = sorted(fea_list)
    out_str = variable_name + " = [" + ",".join(["'" + str(x) + "'" for x in fea_list_sort]) + "]"
    print (out_str)

all_fea_sort = sorted(all_fea)

#for key in all_fea_sort:
#    print (key)
