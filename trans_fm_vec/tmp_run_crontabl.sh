#!/bin/bash
export PATH="/home/appops/anaconda3/bin:$PATH"
source activate
conda activate yanfang

#bash ./run.sh
bash ./tmp_get_fmvec.sh
