#!/bin/sh

# input file
name2cui_umls="/shared/data/mengqu2/umls/cotype/name2cui_umls.txt"
name2cui_go="/shared/data/mengqu2/umls/cotype/name2cui_go.txt"
cui2type_umls="/shared/data/mengqu2/umls/cotype/cui2type_umls.txt"
cui2type_go="/shared/data/mengqu2/umls/cotype/cui2type_go.txt"
pair2relation="/shared/data/mengqu2/umls/cotype/pair2relation.txt"
text_file="text.txt"
training_instance_file="instance_pubmed.txt"

# output file
output_json_file="data_pubmed.json"

python entity_detection.py ${name2cui_umls} ${name2cui_go} ${pair2relation} ${text_file} temp.json stopwords.txt ${training_instance_file}
python map_type.py ${cui2type_umls} ${cui2type_go} temp.json ${output_json_file}

rm -rf temp.json