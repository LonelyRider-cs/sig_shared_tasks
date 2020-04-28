import csv


ALL_LANGUAGE_ABBREVIATIONS = ["arm", "bul", "fre", "geo", "gre", "hin", "hun", "ice", "kor", "lit"]

#for training data
def extract_train():
    f_src = open("complete_aug_train_src.txt", "w")
    f_tgt = open("complete_aug_train_tgt.txt", "w")
    for temp_lang in ALL_LANGUAGE_ABBREVIATIONS:
        with open("data/train_aug/" + temp_lang + "_train_aug.tsv") as tsvfile:
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
def extract_dev_and_test():
    switch = 0
    f_dev_src = open("complete_aug_dev_src.txt", "w")
    f_dev_tgt = open("complete_aug_dev_tgt.txt", "w")

    f_test_src = open("complete_aug_test_src.txt", "w")
    f_test_tgt = open("complete_aug_test_tgt.txt", "w")
    for temp_lang in ALL_LANGUAGE_ABBREVIATIONS:
        with open("data/dev_aug/" + temp_lang + "_dev_aug.tsv") as tsvfile:
            reader = csv.reader(tsvfile, dialect='excel-tab')
            for row in reader:
                temp_transform_grapheme = temp_lang + " "
                for ch in row[0]:
                    temp_transform_grapheme = temp_transform_grapheme + ch + " "
                temp_transform_grapheme += temp_lang
                temp_transform_phoneme = temp_lang + " " + row[1] + " " + temp_lang
                if switch == 0:
                    f_dev_src.write(temp_transform_grapheme + "\n")
                    f_dev_tgt.write(temp_transform_phoneme + "\n")
                    switch = 1
                else:
                    f_test_src.write(temp_transform_grapheme + "\n")
                    f_test_tgt.write(temp_transform_phoneme + "\n")
                    switch = 0
    f_dev_src.close()
    f_dev_tgt.close()

    f_test_src.close()
    f_test_tgt.close()

extract_train()
extract_dev_and_test()
