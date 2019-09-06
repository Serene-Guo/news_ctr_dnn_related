import json

embed_4_32 = "./feature_conf_emb32.json"
embed_old = "./feature_conf.json"

embed_8_32 = "./feature_conf_emb_min8.json"

embed_history="./feature_conf.json.add.user.click.history"

#layers= [512, 256, 128]
layers= [1024, 512, 256]

embed_file = embed_history
#embed_file = embed_8_32
#embed_file = embed_4_32

f_fea = open(embed_file, "r")


fea_list = json.load(f_fea)


print (type(fea_list))
print (len(fea_list))
fea_total_num = 0
fea_conti = 0
discrete_fea = 0
discrete_fea_dict = {}
fix_fea = 0
fix_fea_dict = {}
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
    
    ## model_desc 
    if "model_desc" not in fea_dict:
        continue
    model_desc = fea_dict["model_desc"]
    if "dnn" not in model_desc and "lookup_table" not in model_desc:
        print ("model_desc {}: " + fea_dict["desc"] + ". " + str(model_desc))
        continue
    
    embedding_size = None
    if "lookup_table" in model_desc:
        look_dict = model_desc["lookup_table"]
        if "embedding_size" in look_dict:
            embedding_size = look_dict["embedding_size"]
    
    if "dnn" in model_desc:
        dnn_dict = model_desc["dnn"]
        if "embedding_size" in dnn_dict:
            embedding_size = dnn_dict["embedding_size"]
    
    
    if "otype" not in fea_dict:
        print ("otype not in fea_dict: " + fea_dict)
        continue
    otype = fea_dict["otype"]
    if otype not in otype_set:
        print ("otype is " + otype)
        continue
    if otype == "Continuous":
        fea_conti += 1
        continue
    
    feature_size = None
    if "feature_size" in fea_dict:
        feature_size = fea_dict["feature_size"]


    if otype == "Discrete":
        if embedding_size is None or feature_size is None:
            print ("embedding_size is none, or feature_size is none. " + fea_dict["desc"] + ". " + str(model_desc))
            continue
        discrete_fea +=1 
        discrete_fea_dict[fea_dict["desc"]] = [feature_size, embedding_size]
        continue
    if otype == "FixedSize":
        if embedding_size is None or feature_size is None:
            print ("embedding_size is none, or feature_size is none. " + fea_dict["desc"] + ". " + str(model_desc))
            continue
        fix_fea +=1 
        if feature_size > 20 * 10000 * 10000:
            continue
        fix_fea_dict[fea_dict["desc"]] = [feature_size, embedding_size]

print ("fea_total_num: %d" % fea_total_num)
print ("fea_conti: %d" % fea_conti)
print ("discrete_fea: %d" % discrete_fea)
print ("fix_fea: %d" % fix_fea)
print ("3 sum: %d" % (fea_conti + discrete_fea + fix_fea))

discrete_input = 0
discrete_embed_params = 0
for key in discrete_fea_dict:
    #print (key + ":" + str(discrete_fea_dict[key]))
    discrete_input += discrete_fea_dict[key][1]
    discrete_embed_params += discrete_fea_dict[key][0] * discrete_fea_dict[key][1]

fix_input = 0
fix_embed_params = 0
for key in fix_fea_dict:
    fix_input += fix_fea_dict[key][1]
    fix_embed_params += fix_fea_dict[key][0] * fix_fea_dict[key][1]
    print ("%s, %d, %d" % (key, fix_fea_dict[key][0], fix_fea_dict[key][1]))
embed_params_total = discrete_embed_params + fix_embed_params

dnn_dense_input_dim = fea_conti + discrete_input + fix_input

hidden_params = 0
for i in range(len(layers)):
    if i == 0:
        in_dim = dnn_dense_input_dim
    else:
        in_dim = layers[i-1]

    out_dim = layers[i]
    
    hidden_params += in_dim * out_dim


print ("continous feature num: %d" % fea_conti)
print ("discrete feature embedding sum: %d" % discrete_input)
print ("fixed_size feature embedding sum: %d" % fix_input)
print ("dnn dense input dim: %d" % dnn_dense_input_dim)

print ("==" * 30)
print ("discrete embed params: %d" % discrete_embed_params)
print ("fix size embed params: %d" % fix_embed_params)
print ("total embed params: %d" % embed_params_total)

print ("==" * 30)
print ("hidden_params: %d" % hidden_params)
print ("embed + hidden params: %d" % (hidden_params + embed_params_total))



