#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
import argparse
import json
import itertools
from datetime import datetime
#from typing import List,Tuple,Set

import os
import struct

MAX_ID_LEN = 95

def get_key_from_origin_fmvec():
    #with open('samp','r') as fin,open('uout','wb')as uout,open('dout','wb')as dout:
    #    for line in fin:
    file_u = "./userid"
    file_d = "./docid"
    with open(file_u,'wb')as uout,open(file_d,'wb')as dout:
        for line in sys.stdin:
            arr = line.strip().split(' ')
            if len(arr) != 196 or len(arr[0]) - 2 > MAX_ID_LEN:
                continue
            head = arr[0][0:2] 
            duid = arr[0][2:].replace('~',':')
            # deal doc
            if head == 'd_' :
                fout = dout
            # deal user
            elif head == 'u_' :
                fout = uout
            else:
                continue

            fout.write(duid)
            fout.write('\n')


def decode_bin():
    index = 0
    input_bin = "./guofangfang_data/20200108/poi"
    output_txt = input_bin + ".txt"
    with open(input_bin, 'rb')as fin,open(output_txt,'w') as fout:
        while True:
            uid = fin.read(96)
            if len(uid)<96:
                break
            uid = uid.strip(b'\x00').decode('utf-8')
            vec = fin.read(64*4)
            vec = struct.unpack('64f',vec)
            #print(uid,vec)
            fout.write(uid.encode('utf-8') + ' ')
            #print (type(uid)) ## uid is unicode, python 2.7.13
            #print (uid)
            for k in vec:
                fout.write("%.8f " % k)
            fout.write('\n')


if __name__ == '__main__':
    decode_bin()
