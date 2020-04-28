import csv


def predicted_strip(pred, gold):
    f_pred = open(pred, "r")
    f_gold = open(gold, "r")
    #fn_pred = open("./model_arm_lstm/stripped_"+pred, "w")
    #fn_gold = open("./model_arm_lstm/stripped_"+pred, "w")

    predicted_lines = f_pred.readlines()
    stripped_pred = []

    for pline in predicted_lines:
        temp =""
        tline = pline[:3]+" "+pline[3:]
        temp = tline.replace('arm', '' )
        temp = temp.replace('bul', '' )
        temp = temp.replace('fre', '' )
        temp = temp.replace('geo', '' )
        temp = temp.replace('gre', '' )
        temp = temp.replace('hin', '' )
        temp = temp.replace('hun', '' )
        temp = temp.replace('ice', '' )
        temp = temp.replace('kor', '' )
        temp = temp.replace('lit', '' )
        temp = temp.replace('\n', '')
        stripped_pred.append(temp)

    gold_lines = f_gold.readlines()
    stripped_gold = []

    for gline in gold_lines:
        temp = ""
        temp = gline.replace('arm', '' )
        temp = temp.replace('bul', '' )
        temp = temp.replace('fre', '' )
        temp = temp.replace('geo', '' )
        temp = temp.replace('gre', '' )
        temp = temp.replace('hin', '' )
        temp = temp.replace('hun', '' )
        temp = temp.replace('ice', '' )
        temp = temp.replace('kor', '' )
        temp = temp.replace('lit', '' )
        temp = temp.replace('\n', '')
        stripped_gold.append(temp)


    with open("./model_2_all_aug/complete_aug_pred_gold_eval.tsv", "w") as tsvfile:

        for i in range(0,len(stripped_pred)):
            tsvfile.write(stripped_gold[i] + "\t" + stripped_pred[i] +"\n")

    f_pred.close()
    #fn_pred.close()
    f_gold.close()
    #fn_gold.close()

predicted_strip("./model_2_all_aug/complete_aug_model_lstm_step_50000_pred", "./model_2_all_aug/complete_aug_test_tgt.txt")
