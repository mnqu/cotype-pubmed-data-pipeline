import sys
import os
import json

mesh_file = sys.argv[1]
pmid2mesh_file = sys.argv[2]
input_json_file = sys.argv[3]
output_json_file = sys.argv[4]

mesh2flag = {}
fi = open(mesh_file, 'r')
for mesh in mesh_file:
	mesh2flag[mesh.strip()] = 1
fi.close()

pmid2flag = {}
fi = open(pmid2mesh_file, 'r')
for line in fi:
	lst = line.strip().split('\t')
	pmid = int(lst[0])
	for k in range(1,len(lst)):
		mesh = lst[k]
		if mesh2flag.get(mesh, 0) == 1:
			pmid2flag[pmid] = 1
fi.close()

fi = open(input_json_file, 'r')
fo = open(output_json_file, 'w')
for line in fi:
	data = json.loads(line.strip())
	pmid = data["articleId"]
	if pmid2flag.get(pmid, 0) == 1:
		fo.write(json.dumps(data) + '\n')
fi.close()
fo.close()

