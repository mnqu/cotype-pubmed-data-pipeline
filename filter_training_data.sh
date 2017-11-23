#!/bin/sh

# data path
umls_path=/shared/data/mengqu2/umls/cotype/

# input file
input_json_file=data_pubmed_abs.json
mesh_file=mesh.txt
pmid2mesh_file=pmid2mesh.txt

# output file
output_json_file=data_pubmed_filter.json

python filter_json_with_mesh.py ${mesh_file} ${pmid2mesh_file} ${input_json_file} ${output_json_file}