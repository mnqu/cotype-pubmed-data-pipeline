#!/bin/sh

# data path
umls_path=/shared/data/mengqu2/umls/cotype/

# NER path
ner_model=${umls_path}stanford-ner/ner_calbc.sh

# input file
# name2cui_umls: Mapping file from UMLS entity name to entity id. Each line of the file contains a name and an id, separated by '\t'.
# name2cui_go: Mapping file from GO entity name to entity id. Each line of the file contains a name and an id, separated by '\t'.
# cui2type_umls: Mapping file from UMLS entity id to entity type. Each line of the file contains an id and a type, separated by '\t'.
# cui2type_go: Mapping file from GO entity id to entity type. Each line of the file contains an id and a type, separated by '\t'.
# pair2relation: Mapping file from entity pair to relation. Each line of the file contains two id and a relation, separated by '\t'.
name2cui_umls=${umls_path}name2cui_umls.txt
name2cui_go=${umls_path}name2cui_go.txt
cui2type_umls=${umls_path}cui2type_umls.txt
cui2type_go=${umls_path}cui2type_go.txt
pair2relation=${umls_path}pair2relation.txt

text_file=text.txt

# output file
output_json_file=data_test.json

${ner_model} ${text_file} text_ner.txt
python process.py text_ner.txt ${name2cui_umls} ${name2cui_go} ${cui2type_umls} ${cui2type_go} ${pair2relation} ${output_json_file}

rm -rf text_ner.txt