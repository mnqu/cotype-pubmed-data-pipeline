#!/bin/sh

# NER path
ner_model="/shared/data/mengqu2/umls/cotype/stanford-ner/ner_calbc.sh"

# input file
name2cui_umls="/shared/data/mengqu2/umls/cotype/name2cui_umls.txt"
name2cui_go="/shared/data/mengqu2/umls/cotype/name2cui_go.txt"
cui2type_umls="/shared/data/mengqu2/umls/cotype/cui2type_umls.txt"
cui2type_go="/shared/data/mengqu2/umls/cotype/cui2type_go.txt"
pair2relation="/shared/data/mengqu2/umls/cotype/pair2relation.txt"

text_file="text.txt"

# output file
output_json_file="data_pubmed.json"

${ner_model} ${text_file} text_ner.txt
python process.py text_ner.txt ${name2cui_umls} ${name2cui_go} ${cui2type_umls} ${cui2type_go} ${pair2relation} ${output_json_file}

rm -rf text_ner.txt