#!/bin/bash

lang_code=$1
src_train="${lang_code}_train_src.txt"
tgt_train="${lang_code}_train_tgt.txt"

src_dev="${lang_code}_dev_src.txt"
tgt_dev="${lang_code}_dev_tgt.txt"

src_test="${lang_code}_test_src.txt"
tgt_test="${lang_code}_test_tgt.txt"

preprocess="${lang_code}_preprocess.low"

model="${lang_code}_model_lstm"
model_translate="${model}_step_50000.pt"

predicted="${model}_step_50000_pred"

python transform_data.py $lang_code

wait

onmt_preprocess -train_src $src_train -train_tgt $tgt_train -valid_src $src_dev -valid_tgt $tgt_dev -save_data $preprocess -lower

wait

onmt_train -data $preprocess -save_model $model -gpu_ranks 0 -train_steps 50000

wait

onmt_translate -gpu 0 -model $model_translate -src $src_test -tgt $tgt_test -replace_unk -verbose -output $predicted
