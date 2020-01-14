import json

embed_4_32 = "./feature_conf_emb32.json"
embed_old = "./feature_conf.json"


embed_8_32 = "./feature_conf_emb_min8.json"

embed_history="./feature_conf.json.add.user.click.history"

embed_gff = "./guofangfang_test_no_timestamp_feature_conf.json"

embed_bai = "./bai_feature_conf.json"


embed_gff= "./guofangfang_test_no_timestamp_V1_feature_conf.json"
embed_CQ = "./history0819_CQ_feature_conf.json"

embed_v3 = "./hourly_earliest_V3_feature_conf.json"
embed_cq_1 = "./all_feature_CQ_1_feature_conf.json"
#layers= [512, 256, 128]

small_embed = "./small_embed.json"
small_embed2 = "./small_embed_0923.json"

new_gauc_fea = "./gauc_base_feature_conf.json"
old_gauc_fea = "./old_gauc_base_feature_conf.json"

layers= [1024, 512, 256]

embed_file = old_gauc_fea
#embed_file = embed_8_32
#embed_file = embed_4_32

f_fea = open(embed_file, "r")


fea_list = json.load(f_fea)

###
##
#    "otype": "Continuous",
#    "otype": "Discrete",
#    "otype": "Double",  doubleToNull, visible=False
#    "otype": "FixedSize",
#    "otype": "Label",
#    "otype": "ListInt32",

fea_total_num = 0
fea_conti = 0
discrete_fea = 0
discrete_fea_dict = {}
fix_fea = 0
fix_fea_dict = {}
otype_set = set(["Continuous", "Discrete", "FixedSize"])

print ("\t".join(["output", "desc", "inputs", "otype", "dnn", "feature_size", "emb_size", "func", "max_len", "visible"]))

for fea_dict in fea_list:
    [output, desc, inputs, otype, dnn, feature_size, emb_size, func, max_len, visible] = ["NULL"] * 10 
     
       
    if "desc" in fea_dict:
        desc = fea_dict["desc"]
    if "output" in fea_dict:
        output = fea_dict["output"]
    
    if "inputs" in fea_dict:
        inputs = ",".join(fea_dict["inputs"])
    if "otype" in fea_dict:
        otype = fea_dict["otype"]
    ## model_desc 
    if "model_desc" not in fea_dict:
        continue
    model_desc = fea_dict["model_desc"]
    
    emb_size_int = 0
    if "lookup_table" in model_desc:
        dnn = "dnn"
        look_dict = model_desc["lookup_table"]
        if "embedding_size" in look_dict:
            emb_size_int = look_dict["embedding_size"]
    
    if "dnn" in model_desc:
        dnn = "dnn"
        dnn_dict = model_desc["dnn"]
        if "embedding_size" in dnn_dict:
            emb_size_int = dnn_dict["embedding_size"]

    emb_size = str(emb_size_int)
    
    feature_size_int = 0
    if "feature_size" in fea_dict:
        feature_size_int = fea_dict["feature_size"]
    feature_size = str(feature_size_int)
    
    if "function" in fea_dict:
        func = fea_dict["function"]
    
    if "max_length" in fea_dict:
        max_len = str(fea_dict["max_length"])

    if "visible" not in fea_dict:
        continue
    visible_bool = fea_dict["visible"]
    if visible_bool:
        visible = "True"
    else:
        visible ="False"

    out_str = "\t".join([output, desc, inputs, otype, dnn, feature_size, emb_size, func, max_len , visible])
    print (out_str)


