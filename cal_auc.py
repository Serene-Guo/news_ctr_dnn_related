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
    print ("total_sample_num:" + str(total_sample_num))
    print ("total_uid_num:" + str(uid_num))

    print ("gauc_sample_num:" + str(gauc_sample_num))
    print ("gauc_uid_num:" + str(gauc_uid_num))
    return sum / counts


uids = []
labels = []
scores = []

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = 'result.txt'

with open(file_name, 'r') as r:
    for line in r.readlines():
        line = line.strip()
        uid, label, score = line.split('\t')[:3]
        uids.append(uid)
        labels.append(int(label))
        scores.append(float(score))

auc = roc_auc_score(labels, scores)
print('AUC: {}'.format(auc))
gauc = gauc_score(uids, labels, scores)
print('GAUC: {}'.format(gauc))
