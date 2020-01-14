import sys
from sklearn.metrics import roc_auc_score


def gauc_score(uids, labels, scores):
    user_dict = {}
    for uid, label, score in zip(uids, labels, scores):
        if uid in user_dict:
            user_dict[uid]['labels'].append(label)
            user_dict[uid]['scores'].append(score)
        else:
            user_dict[uid] = {}
            user_dict[uid]['labels'] = [label]
            user_dict[uid]['scores'] = [score]
    counts = 0
    sum = 0.0
    total_sample_num = 0
    gauc_sample_num = 0
    uid_num = 0
    gauc_uid_num = 0
    for uid, value in user_dict.items():
        count = len(value['labels'])
        total_sample_num += count
        uid_num += 1
        try:
            auc = roc_auc_score(value['labels'], value['scores'])
        except ValueError:
            continue
        gauc_sample_num += count
        gauc_uid_num = 0

        sum += auc * count
        counts += count
    
    #print ("total_sample_num:" + str(total_sample_num))
    #print ("total_uid_num:" + str(uid_num))

    #print ("gauc_sample_num:" + str(gauc_sample_num))
    #print ("gauc_uid_num:" + str(gauc_uid_num))
    return sum / counts, total_sample_num, uid_num, gauc_sample_num, gauc_uid_num


#uids = []
#labels = []
#scores = []

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = 'result.txt'

auc_dict = {}
with open(file_name, 'r') as r:
    for line in r.readlines():
        line = line.strip()
        uid, label, score, model_name = line.split('\t')[:4]
        if score == "NULL":
            pass
            #continue
        if model_name not in auc_dict:
            auc_dict[model_name] = ([], [], [])
        uids, labels, scores = auc_dict[model_name]
        uids.append(uid)
        labels.append(int(label))
        scores.append(float(score))

for model in auc_dict:
    print ("\t".join(["model", "auc", "gauc", "total_sample_num", "total_uid_num", "gauc_sample_num", "gauc_uid_num"]))
    uids, labels, scores = auc_dict[model]

    auc = roc_auc_score(labels, scores)
    auc = float("%.6f" % auc)
    #print('AUC: {}'.format(auc))
    gauc, total_sample_num, uid_num, gauc_sample_num, gauc_uid_num = gauc_score(uids, labels, scores)
    gauc = float("%.6f" % gauc)
    #print('GAUC: {}'.format(gauc))
    print ("\t".join([model] + [str(x) for x in [auc, gauc, total_sample_num, uid_num, gauc_sample_num, gauc_uid_num]]))
