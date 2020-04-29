import csv
import sys

ALL_LANGUAGE_ABBREVIATIONS = ["ady", "arm", "bul", "dut", "fre", "geo", "gre", "hin", "hun", "ice", "jpn", "kor", "lit", "rum", "vie"]
#ALL_LANGUAGE_ABBREVIATIONS = [str(sys.argv[1])]
print(ALL_LANGUAGE_ABBREVIATIONS)

#for training data
def extract_train():

    for temp_lang in ALL_LANGUAGE_ABBREVIATIONS:
        f_src = open("model_"+temp_lang+"_lstm/"+temp_lang+"_train_src.txt", "w")
        f_tgt = open("model_"+temp_lang+"_lstm/"+temp_lang+"_train_tgt.txt", "w")
        with open("data/train/" + temp_lang + "_train.tsv") as tsvfile:
            reader = csv.reader(tsvfile, dialect='excel-tab')
            for row in reader:
                temp_transform_grapheme = temp_lang + " "
                for ch in row[0]:
                    temp_transform_grapheme = temp_transform_grapheme + ch + " "
                temp_transform_grapheme += temp_lang
                f_src.write(temp_transform_grapheme+"\n")

                temp_transform_phoneme = temp_lang + row[1] + " " + temp_lang
                f_tgt.write(temp_transform_phoneme+"\n")
    f_src.close()
    f_tgt.close()

#for dev data
def extract_dev():
    switch = 0

    for temp_lang in ALL_LANGUAGE_ABBREVIATIONS:
        f_dev_src = open("model_"+temp_lang+"_lstm/"+temp_lang+"_dev_src.txt", "w")
        f_dev_tgt = open("model_"+temp_lang+"_lstm/"+temp_lang+"_dev_tgt.txt", "w")


        with open("data/dev/" + temp_lang + "_dev.tsv") as tsvfile:
            reader = csv.reader(tsvfile, dialect='excel-tab')
            for row in reader:
                temp_transform_grapheme = temp_lang + " "
                for ch in row[0]:
                    temp_transform_grapheme = temp_transform_grapheme + ch + " "
                temp_transform_grapheme += temp_lang
                temp_transform_phoneme = temp_lang + " " + row[1] + " " + temp_lang

                f_dev_src.write(temp_transform_grapheme + "\n")
                f_dev_tgt.write(temp_transform_phoneme + "\n")


    f_dev_src.close()
    f_dev_tgt.close()


#for dev data
def extract_test():
    switch = 0

    for temp_lang in ALL_LANGUAGE_ABBREVIATIONS:
        f_test_src = open("model_"+temp_lang+"_lstm/"+temp_lang+"_test_src.txt", "w")
        #f_test_tgt = open("model_"+temp_lang+"_lstm/"+temp_lang+"_test_tgt.txt", "w")


        with open("data/test/" + temp_lang + "_test.txt") as txtfile:
            reader = csv.reader(txtfile)
            for row in reader:
                temp_transform_grapheme = temp_lang + " "
                for ch in row[0]:
                    temp_transform_grapheme = temp_transform_grapheme + ch + " "
                temp_transform_grapheme += temp_lang
                #temp_transform_phoneme = temp_lang + " " + row[1] + " " + temp_lang

                f_test_src.write(temp_transform_grapheme + "\n")
                #f_test_tgt.write(temp_transform_phoneme + "\n")


    f_test_src.close()
    #f_test_tgt.close()


#extract_train()
#extract_dev()
extract_test()
