#!/bin/sh

# data path
umls_path=/shared/data/mengqu2/umls/cotype/

# input file
name2cui_umls=${umls_path}name2cui_umls.txt
name2cui_go=${umls_path}name2cui_go.txt
cui2type_umls=${umls_path}cui2type_umls.txt
cui2type_go=${umls_path}cui2type_go.txt
pair2relation=${umls_path}pair2relation.txt
text_file=${umls_path}pubmed.token

# output file
output_json_file="data_pubmed.json"
output_instance_file="instance_pubmed.txt"

python distant_supervision.py ${name2cui_umls} ${name2cui_go} ${pair2relation} ${text_file} temp.json stopwords.txt ${output_instance_file}
python map_type.py ${cui2type_umls} ${cui2type_go} temp.json ${output_json_file}

rm -rf temp.json