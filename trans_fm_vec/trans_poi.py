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
import os
import struct
import numpy as np

MAX_ID_LEN = 95

def encode_bin(path_base, filename):
    #with open('samp','r') as fin,open('uout','wb')as uout,open('dout','wb')as dout:
    #    for line in fin:
    file_p = os.path.join(path_base,'poi',filename)
    file_c = os.path.join(path_base,'cat',filename)
    file_s = os.path.join(path_base,'source_name',filename)
    file_k = os.path.join(path_base,'keyword',filename)
    poi_set = set()
    with open(file_p,'wb')as pout,open(file_c,'wb')as cout, open(file_s, 'wb') as sout, open(file_k, 'wb') as kout:
        for line in sys.stdin:
            arr = line.strip().split(' ')
            if len(arr) != 196:
                continue
            head = arr[0][0:2]
            if head =='u_':
                # devid, pass
                continue
            ### revert replace from hongbin. devid .replaceAll(":","~").replaceAll(" ","!") 
            # duid = arr[0][2:].replace('~',':').replace("!", " ") 
            ##  d_s_ source_name
            ##  d_p_ poi
            ##  d_k_ keyword
            ##  d_c_  cat
            head = arr[0][0:4] 
            if len(arr[0]) - 4 > MAX_ID_LEN:
                continue
            
            vec_key = arr[0][4:]
            ## arr[2:66])  
            fm_vec_64 = np.array(arr[2:66]).astype(np.float32) 
            vec_byte = struct.pack('=64f',*fm_vec_64)
            
             
            if head == 'd_p_' :
                ## poi
                fout = pout
                poi_arr = vec_key.split("_")
                if len(poi_arr) < 2:
                    continue
                poi_without_prefix = poi_arr[1]
                if poi_without_prefix in poi_set:
                    ### poi deduplicate
                    continue
                poi_set.add(poi_without_prefix)
                vec_key_byte = bytes(poi_without_prefix, encoding = "utf-8")
            elif head == 'd_k_' :
                fout = kout
                vec_key_byte = bytes(vec_key, encoding = "utf-8")
            elif head == 'd_c_' :
                fout = cout
                cat_arr = vec_key.split("/")
                if len(cat_arr) >= 2:
                    ##  / is ditry data
                    continue
                vec_key = vec_key.replace('_', '/')  ## _ to /
                vec_key_byte = bytes(vec_key, encoding = "utf-8")
            elif head == 'd_s_' :
                fout = sout
                vec_key_byte = bytes(vec_key, encoding = "utf-8")
            else:
                continue
            
            ###  filter,   max 95 + \0 char. is key  when load table.
            if len(vec_key_byte)>95 :
                continue
            fout.write(vec_key_byte)
            fout.write(bytes(96-len(vec_key_byte)))
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
    if len(sys.argv) < 3:
        print("args not enough!")
    base_dir = sys.argv[1]
    filename = sys.argv[2]
    os.system(f"mkdir -p {base_dir}/cat/")
    os.system(f"mkdir -p {base_dir}/poi/")
    os.system(f"mkdir -p {base_dir}/source_name/")
    os.system(f"mkdir -p {base_dir}/keyword")
    encode_bin(base_dir, filename)
