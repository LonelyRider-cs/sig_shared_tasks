# 2020

**SIGMORPHON 2020 Shared Task 1 CU-Z Model (g2paugment.py) **

A data-augmentation strategy for grapheme-to-phoneme (G2P), as applied to the SIGMORPHON 2020 shared task 1:

```
@inproceedings{ryan2020sigmorphon, 
    title={Data Augmentation for Transformer-based G2P}, 
    author={Ryan, Zach and Hulden, Mans}, 
    booktitle={Proceedings of the 17th SIGMORPHON Workshop on Computational Research in Phonetics, Phonology, and Morphology},
    year={2020}
}
```

## Compile

Run `make`. This builds the alignment library libalign.so needed by `g2paugment.py`. Requires gcc.

## Run

The script reads training data files in the `.tsv`-format used in the 2020 shared task 1 on G2P. It outputs an augmented data set from some subset of the training data.

## Example

```./g2paugment.py task1/data/train/fre_train.tsv -i 100 -o 10000```

would run the augmentation on French training data and generate 10000 example pairs from 100 randomly chosen examples in the original data set. The augmented examples are printed to stdout.

## Options

```
 Usage: g2paugment.py [OPTIONS] tsvfile
 -o NUM     How many output examples to create (default: 50000)")
 -i NUM     How many input examples to use when augmenting (default: 100)")
 -r NUM     Set random seed (default: 42)")
 -m NUM     maximum length words to create when augmenting (default: 15)")
 -c NUM     Cutoff for confidence in in-out mapping slices (default: 0.98)")
 -d         Duplicate the original examples used in the output (default: no)")
 ```

## Results

The following figure shows roughly what kind of performance to expect with the augmentation strategy. The models were trained with the fairseq Transformer model. See paper for training details.

![Results](./augmentresults.png?raw=true "Results")





