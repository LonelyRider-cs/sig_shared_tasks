#!/bin/bash

#lang_code=$1
#all_langs=("ady" "arm" "bul" "dut" "fre" "geo" "gre" "hin" "hun" "ice" "jpn" "kor" "lit" "rum" "vie")
all_langs=("fre" "kor")
for lang_code in ${all_langs[@]};
do
  src_train="./model_${lang_code}_lstm/${lang_code}_train_src.txt"
  tgt_train="./model_${lang_code}_lstm/${lang_code}_train_tgt.txt"
  echo $src_train
  src_test="./model_${lang_code}_lstm/${lang_code}_dev_src.txt"
  tgt_test="./model_${lang_code}_lstm/${lang_code}_dev_tgt.txt"
  echo $src_dev
  #src_test="./model_${lang_code}_lstm/${lang_code}_test_src.txt"
  #tgt_test="./model_${lang_code}_lstm/${lang_code}_test_tgt.txt"

  preprocess="./model_${lang_code}_lstm/${lang_code}_preprocess.low"

  model="./model_${lang_code}_lstm/${lang_code}_model_lstm"
  model_translate="${model}_step_50000.pt"
  echo $model_translate
  predicted="${model}_step_50000_pred_10_best_dev"

  #uncomment if language needs to format for openNMT
  #python transform_data.py $lang_code

  #wait

  #onmt_preprocess -train_src $src_train -train_tgt $tgt_train -valid_src $src_dev -valid_tgt $tgt_dev -save_data $preprocess -lower

  #wait

  #onmt_train -data $preprocess -save_model $model -gpu_ranks 0 -train_steps 50000

  #wait

  #onmt_translate -gpu 0 -model $model_translate -src $src_test -tgt $tgt_test -replace_unk -verbose -output $predicted
  onmt_translate -gpu 0 -model $model_translate -src $src_test -tgt $src_test -replace_unk -verbose -n_best 10 -output $predicted

  #wait
done
