#!/bin/sh

# data path
umls_path=/shared/data/mengqu2/umls/cotype/

# NER path
ner_model=${data_path}stanford-ner/ner_calbc.sh

# input file
name2cui_umls=${umls_path}name2cui_umls.txt
name2cui_go=${umls_path}name2cui_go.txt
cui2type_umls=${umls_path}cui2type_umls.txt
cui2type_go=${umls_path}cui2type_go.txt
pair2relation=${umls_path}pair2relation.txt

text_file="text.txt"

# output file
output_json_file="data_pubmed.json"

${ner_model} ${text_file} text_ner.txt
python process.py text_ner.txt ${name2cui_umls} ${name2cui_go} ${cui2type_umls} ${cui2type_go} ${pair2relation} ${output_json_file}

rm -rf text_ner.txt