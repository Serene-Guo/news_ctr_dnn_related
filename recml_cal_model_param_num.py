import json

embed_4_32 = "./feature_conf_emb32.json"
embed_old = "./feature_conf.json"

embed_8_32 = "./feature_conf_emb_min8.json"

embed_history="./feature_conf.json.add.user.click.history"

feature_conf_file = './feature_confs/gff_v0_0327_feature_conf.json'
#feature_conf_file = './feature_confs/xjg_video_v13_feature_conf.json'

#feature_conf_file = './feature_confs/wjh_v13_feature_conf.json'

#layers= [512, 256, 128]
layers= [1024, 512, 256]

embed_file = feature_conf_file
#embed_file = embed_8_32
#embed_file = embed_4_32

f_fea = open(embed_file, "r")


fea_list = json.load(f_fea)


print (len(fea_list))

fea_total_num = 0

#fea_conti = 0
dnn_conti_fea = 0
linear_conti_fea = 0

#discrete_fea = 0
#discrete_fea_dict = {}
#fix_fea = 0
#fix_fea_dict = {}

dnn_discrete_fea = 0
dnn_discrete_fea_dict = {}
dnn_fix_fea = 0
dnn_fix_fea_dict = {}

linear_discrete_fea = 0
linear_discrete_fea_dict = {}
linear_fix_fea = 0
linear_fix_fea_dict = {}



otype_set = set(["Continuous", "Discrete", "FixedSize"])

for fea_dict in fea_list:
    if "visible" not in fea_dict:
        print (fea_dict)
        continue
    visible = fea_dict["visible"]
    if visible:
        fea_total_num += 1
    else:
        print ("[%s] not visible" % fea_dict["desc"])
        continue
    
       
    
    
    ## process model_desc 
    if "model_desc" not in fea_dict:
        continue
    model_desc = fea_dict["model_desc"]
    if len(model_desc) == 0:
        print ("[%s] model_desc is null." % fea_dict["desc"])
        continue
    if "modules" not in model_desc:
        print ("[%s] no modules in model_desc." % fea_dict['desc'])
        continue
    if "preprocess" not in model_desc:
        print ("[%s] no preprocess in model_desc." % fea_dict['desc'])
        continue
    
    preprocess_dict = {}
    prep_conf_dict = model_desc['preprocess']
    if len(prep_conf_dict) == 0:
        print ("[%s] preprocess len = 0" % fea_dict['desc'])
        continue
    #print (fea_dict['desc'] )
    #print (prep_conf_dict)
    for (key, v_dict) in prep_conf_dict.items():
        #v_dict = prep_conf_dict[key]
        embedding_size = 0
        feature_size = 0
        if 'embedding_size' in v_dict:
            embedding_size = v_dict['embedding_size']
        
        if 'feature_size' in v_dict:
            feature_size = v_dict['feature_size']
        
        ### calibrate the feature_size
        if 'mod_size' in v_dict:
            feature_size = v_dict['mod_size']
         
        if 'table_size' in v_dict and 'extend_size' in v_dict:
            feature_size = v_dict['table_size'] + v_dict['extend_size']
        
        preprocess_dict[key] = [feature_size, embedding_size]

    modules = model_desc['modules']
    dnn_emb_list = []
    linear_emb_list = []
    for module, v_list in modules.items():
        #v_list = modules[module]
        if module == 'dnn':
            for key in v_list:
                ### tuple
                dnn_emb_list.append((preprocess_dict[key][0], preprocess_dict[key][1]))
        if module == 'linear':
            for key in v_list:
                linear_emb_list.append((preprocess_dict[key][0], preprocess_dict[key][1])) 
    
    if "otype" not in fea_dict:
        print ("otype not in fea_dict: " + fea_dict)
        continue
    otype = fea_dict["otype"]
    if otype not in otype_set:
        print ("otype is " + otype)
        continue
    if otype == "Continuous":
        if len(dnn_emb_list) > 0:
            dnn_conti_fea += 1
        if len(linear_emb_list) > 0:
            linear_conti_fea += 1
        continue
    
    if otype == "Discrete":
        if len(dnn_emb_list) > 0:
            dnn_discrete_fea +=1 
            dnn_discrete_fea_dict[fea_dict["desc"]] = dnn_emb_list
        if len(linear_emb_list) > 0:
            linear_discrete_fea += 1
            linear_discrete_fea_dict[fea_dict["desc"]] = linear_emb_list
        continue
    
    if otype == "FixedSize":
        if len(dnn_emb_list) > 0:
            dnn_fix_fea +=1 
            dnn_fix_fea_dict[fea_dict["desc"]] = dnn_emb_list
        if len(linear_emb_list) > 0:
            linear_fix_fea += 1
            linear_fix_fea_dict[fea_dict["desc"]] = linear_emb_list
        continue



#discrete_input = 0

lin_disc_emb_params = 0
for key, emb_list in linear_discrete_fea_dict.items():
    #print (key + ":" + str(discrete_fea_dict[key]))
    #discrete_input += discrete_fea_dict[key][1]
    out_str = key
    i = 0
    each_fea_params = 0
    for emb_tuple in emb_list:
        lin_disc_emb_params += emb_tuple[0] * emb_tuple[1]
        each_fea_params +=  emb_tuple[0] * emb_tuple[1]
        if i == 0:
            out_str += "\t"
        else:
            out_str += ","
        out_str += ("%d * %d" % (emb_tuple[0], emb_tuple[1]) )
    print ('linear_dis:\t' + out_str + "\t" + str(each_fea_params))

lin_fix_emb_params = 0
for key, emb_list in linear_fix_fea_dict.items():
    #print (key + ":" + str(discrete_fea_dict[key]))
    #discrete_input += discrete_fea_dict[key][1]
    out_str = key
    i = 0
    each_fea_params = 0
    for emb_tuple in emb_list:
        lin_fix_emb_params += emb_tuple[0] * emb_tuple[1]
        each_fea_params +=  emb_tuple[0] * emb_tuple[1]
        if i == 0:
            out_str += "\t"
        else:
            out_str += ","
        out_str += ("%d * %d" % (emb_tuple[0], emb_tuple[1]) )
    print ('linear_fix:\t' + out_str + "\t" + str(each_fea_params))


dnn_disc_emb_params_total = 0
dnn_disc_to_dnn_input = 0
for key, emb_list in dnn_discrete_fea_dict.items():
    #print (key + ":" + str(discrete_fea_dict[key]))
    #discrete_input += discrete_fea_dict[key][1]
    out_str = key
    i = 0
    each_fea_emb_params = 0
    for emb_tuple in emb_list:
        dnn_disc_to_dnn_input += emb_tuple[1]
        dnn_disc_emb_params_total += emb_tuple[0] * emb_tuple[1]
        each_fea_emb_params += emb_tuple[0] * emb_tuple[1]
        if i == 0:
            out_str += "\t"
        else:
            out_str += ","
        out_str += ("%d * %d" % (emb_tuple[0], emb_tuple[1]) )
    print ('dnn_dis\t' + out_str + "\t" + str(each_fea_emb_params))

dnn_fix_emb_params_total = 0
dnn_fix_to_dnn_input = 0
for key, emb_list in dnn_fix_fea_dict.items():
    ### print each feature, embed size
    out_str = key
    i = 0
    each_fea_emb_params = 0
    for emb_tuple in emb_list:
        dnn_fix_to_dnn_input += emb_tuple[1]
        dnn_fix_emb_params_total += emb_tuple[0] * emb_tuple[1]
        each_fea_emb_params += emb_tuple[0] * emb_tuple[1]
        
        if i == 0:
            out_str += "\t"
        else:
            out_str += ","
        out_str += ("%d * %d" % (emb_tuple[0], emb_tuple[1]) )
    print ('dnn_fix\t' + out_str + "\t" + str(each_fea_emb_params))


lin_embed_param_total = lin_disc_emb_params + lin_fix_emb_params
dnn_embed_param_total = dnn_disc_emb_params_total + dnn_fix_emb_params_total


dnn_dense_input_dim = dnn_conti_fea + dnn_disc_to_dnn_input + dnn_fix_to_dnn_input
# linear_dense_input = 

hidden_params = 0
for i in range(len(layers)):
    if i == 0:
        in_dim = dnn_dense_input_dim
    else:
        in_dim = layers[i-1]

    out_dim = layers[i]
    
    hidden_params += in_dim * out_dim


print ("==" * 30)
print ("visible fea_total_num, including modules is null: %d" % fea_total_num)
print ("linear fea_conti: %d" % linear_conti_fea)
print ("linear discrete_fea: %d" % linear_discrete_fea)
print ("linear fix_fea: %d" % linear_fix_fea)
print ("linear 3 sum: %d" % (linear_conti_fea + linear_discrete_fea + linear_fix_fea))

print ("dnn fea_conti: %d" % dnn_conti_fea)
print ("dnn discrete_fea: %d" % dnn_discrete_fea)
print ("dnn fix_fea: %d" % dnn_fix_fea)
print ("dnn 3 sum: %d" % (dnn_conti_fea + dnn_discrete_fea + dnn_fix_fea))


print ('==' * 10 + 'linear model ' + '==' * 10)
print ("continous feature num: %d" % linear_conti_fea)
print ("linear discrete embed params: %d" % lin_disc_emb_params)
print ("linear fix_size embed params: %d" % lin_fix_emb_params)
print ("linear embedding params total: %d" %  lin_embed_param_total)

#print ("==" * 30)
print ('==' * 10 + 'dnn model ' + '==' * 10)
print ("continous feature num: %d" % dnn_conti_fea)
print ("dnn discrete embed params: %d" % dnn_disc_emb_params_total)
print ("dnn fix_size embed params: %d" % dnn_fix_emb_params_total)
print ("dnn total embed params: %d" % dnn_embed_param_total)
print ('dnn dense input dim: %d' % dnn_dense_input_dim)


print ("==" * 30)
print ("hidden_params: %d" % hidden_params)
print ("embed + hidden params: %d" % (hidden_params + dnn_embed_param_total))


