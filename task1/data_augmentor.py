import csv


ALL_LANGUAGE_ABBREVIATIONS = ["arm", "bul", "fre", "geo", "gre", "hin", "hun", "ice", "kor", "lit"]
Data_type = ["dev", "train"]

def main_augmentor():
    #iterate through all language files, train and dev
    for temp_data_type in Data_type:
        for temp_lang in ALL_LANGUAGE_ABBREVIATIONS:
            #dict will hold a dictionary of keys=grapheme values=[count, phonemes]
            dict_front = {}
            dict_back = {}
            #key_set will hold a set of all possible graphemes for the language
            key_set_front = set()
            key_set_back = set()
            with open("data/" + temp_data_type + "/" + temp_lang + "_" + temp_data_type + ".tsv") as tsvfile:
                reader = csv.reader(tsvfile, dialect='excel-tab')
                for row in reader:
                    grapheme = row[0].replace(' ', '').replace('\n', '')
                    phoneme = row[1].replace(' ', '').replace('\n', '')

                    #keys to use for dictionary
                    keys_front = [grapheme[:1], grapheme[:1]+"="+phoneme[:1]]
                    keys_back = [grapheme[-1:], grapheme[-1:]+"="+phoneme[-1:]]
                    #creates a dictonary where the keys are the first letter of the grapheme
                    #and grapheme=phoneme, the values the count and set of all phonemes the grapheme uses
                    key_set_front.add(grapheme[:1])
                    key_set_back.add(grapheme[-1:])
                    for key in keys_front:
                        if key in dict_front.keys():
                            dict_front[key][0] += 1
                            dict_front[key][1].add(phoneme[:1])
                        else:
                            dict_front[key] = [1, set(phoneme[:1])]
                    for key in keys_back:
                        if key in dict_back.keys():
                            dict_back[key][0] += 1
                            dict_back[key][1].add(phoneme[-1:])
                        else:
                            dict_back[key] = [1, set(phoneme[-1:])]
            aug_pairs_front = is_augmentable(key_set_front, dict_front)
            aug_pairs_back = is_augmentable(key_set_back, dict_back)
            #print(key_set)
            #print(dict)
            augment_data(aug_pairs_front, aug_pairs_back, temp_data_type, temp_lang)


#checks to see if all (grapheme, phoneme) tuples are augmentable, if so it is returned in the array
def is_augmentable(key_set, dict):
    augmentable_pair = []
    #iterate through all keys found
    for key in key_set:
        #get the graphemes total count it shows up
        total_grapheme_count = dict[key][0]
        #get all possible phonemes the grapheme can have
        phoneme_set = dict[key][1]
        #iterate through all phonemes to get grapheme=phoneme key for dict
        for pho in phoneme_set:
            #check the dictionary
            if key+"="+pho in dict.keys():
                phoneme_count = dict[key+"="+pho][0]
                #if the grapheme maps to a phoneme more 95% of the time or more it is considered augmentable
                percent_mapped = (phoneme_count*1.00)/(total_grapheme_count*1.00)
                if percent_mapped >= 0.95:
                    augmentable_pair.append((key, pho))
    #print(augmentable_pair)
    return augmentable_pair

def augment_data(aug_pairs_front, aug_pairs_back, temp_data_type, temp_lang):
    augmented_data = set()
    #create file to write augmented data to
    with open("data/"+ temp_data_type+"_aug/"+temp_lang+"_"+temp_data_type+"_aug.tsv", "w") as tsvfile_write:
        writer = csv.writer(tsvfile_write, dialect='excel-tab', delimiter='\t')
        #open file to read from
        with open("data/" + temp_data_type + "/" + temp_lang + "_" + temp_data_type + ".tsv") as tsvfile_read:
            reader = csv.reader(tsvfile_read, dialect='excel-tab')
            for row in reader:
                grapheme = row[0]
                phoneme = row[1]
                #check to see if the current rows grapheme and phonemes first character is in the augmentable pairs set
                #if it is, iterate through all pairs and augment the data, added to set to ensure no duplicates are created
                if (grapheme[:1], phoneme[:1]) in aug_pairs_front:
                    for pair_front in aug_pairs_front:
                        augmented_data.add((pair_front[0]+grapheme[1:], pair_front[1]+phoneme[1:]))
                #check to see if the current rows grapheme and phonemes last character is in the augmentable pairs set
                #if it is, iterate through all pairs and augment the data, added to set to ensure no duplicates are created
                elif (grapheme[-1:], phoneme[-1:]) in aug_pairs_back:
                    for pair_back in aug_pairs_back:
                        augmented_data.add((grapheme[:-1]+pair_back[0], phoneme[:-1]+pair_back[1]))
                #if the first or last characters are not found in the pairs, dont do anything to the row
                #and simply added it to the set to ensure no duplicates
                else:
                    augmented_data.add((grapheme, phoneme))
        #iterates through the new set of augmented data, changes each grapheme-phoneme pair into an array and adds to new file
        for line in augmented_data:
            temp_row = [line[0], line[1]]
            writer.writerow(temp_row)


if __name__ == '__main__':
    main_augmentor()
