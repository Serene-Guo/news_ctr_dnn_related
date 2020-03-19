#!/bin/bash
export PATH="/home/appops/anaconda3/bin:$PATH"
source activate
conda activate yanfang

#bash ./run.sh
bash ./run_get_poi_cat_vec.sh
