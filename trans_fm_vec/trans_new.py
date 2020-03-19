#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
import argparse
import json
import itertools
from datetime import datetime
from typing import List,Tuple,Set

#import mmh3
import jpype
from jpype import *
import os
import struct
import numpy as np

MAX_ID_LEN = 95
UID_HASH_SEED = 171
UID_BUCKET = set([24,54] + list(range(31,34))) #24,54,55,60


def load_devid_set(devid_file):
    #devid_file = "./devid_data/devid_2019-11-19.txt"
    devid_set = set()
    f_in = open(devid_file, "r")
    for line in f_in:
        line = line.strip()
        line_arr = line.split('\t')
        if len(line_arr) < 3:
            continue
        devid = line_arr[2]
        devid_set.add(devid)
    return devid_set


#return abs(mmh3.hash(uid, seed = UID_HASH_SEED)) % 100 in UID_BUCKET
#return hashObj.getToutiaoBucket(uid)%100 in UID_BUCKET 

def encode_bin(path_base,filename, devid_file):
    #with open('samp','r') as fin,open('uout','wb')as uout,open('dout','wb')as dout:
    #    for line in fin:
    DEVID_SET = load_devid_set(devid_file)
    def isValidUid(uid):
        return (uid in DEVID_SET)
    
    file_u = os.path.join(path_base,'user',filename)
    file_d = os.path.join(path_base,'doc',filename)
    with open(file_u,'wb')as uout,open(file_d,'wb')as dout:
        for line in sys.stdin:
            arr = line.strip().split(' ')
            if len(arr) != 196 or len(arr[0]) - 2 > MAX_ID_LEN:
                continue
            head = arr[0][0:2] 
            ### revert replace from hongbin..replaceAll(":","~").replaceAll(" ","!") 
            duid = arr[0][2:].replace('~',':').replace("!", " ") 
            

            vec = np.array(arr[2:66]).astype(np.float32) 
            vec_byte = struct.pack('=64f',*vec)

            # deal doc
            if head == 'd_' :
                fout = dout
                ### docid do not encrypt !!
                duid_byte = bytes(duid, encoding = "utf-8")
            # deal user
            elif head == 'u_' :
                fout = uout
                if not isValidUid(duid):
                    continue
                ### devid need encrypt !!
                duid_encrypt = encode_java_obj.encrypt(duid)
                duid_byte = bytes(duid_encrypt, encoding = "utf-8")
            else:
                continue
            
            ### why filter, dnn load vec, key_size=96
            if len(duid_byte)>95 :
                continue
            fout.write(duid_byte)
            fout.write(bytes(96-len(duid_byte)))
            fout.write(vec_byte)

def decode_bin():
    index = 0
    with open('./user','rb')as fin,open('user_2019-11-19_encrypt_new_user.txt','w') as fout:
        while True:
            uid = fin.read(96)
            if len(uid)<96:
                break
            uid = uid.strip(b'\x00').decode('utf-8')
            vec = fin.read(64*4)
            vec = struct.unpack('64f',vec)
            #print(uid,vec)
            fout.write('u_' + uid + ' ')
            for k in vec:
                fout.write("%.8f" % k)
            fout.write('\n')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("args not enough!")
        sys.exit(1)
    base_dir = sys.argv[1]
    filename = sys.argv[2]
    devid_file = sys.argv[3]

    os.system(f"mkdir -p {base_dir}/user")
    os.system(f"mkdir -p {base_dir}/doc")
    jvmPath = jpype.getDefaultJVMPath()
    dependency = os.path.join(os.path.abspath('.'), '/home/appops/fmvec/hash-util')
    jpype.startJVM(jvmPath, "-Djava.ext.dirs=%s" %dependency)
    #hashObj=JClass("com.netease.rec.news.engine.util.HashUtil")
    encode_java_obj = JClass("com.netease.recsys.urs.util.UrsEncoder")
    encode_bin(base_dir, filename, devid_file)
    jpype.shutdownJVM()
