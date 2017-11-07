import sys
import os
import json

# mapping cui to entity types
cui2type = {}
fi = open(sys.argv[1], 'r')
for line in fi:
	try:
		cui = line.strip().split('\t')[0]
		tp = line.strip().split('\t')[1].replace(' ', '_')
	except IndexError:
		continue
	if cui2type.get(cui, None) == None:
		cui2type[cui] = {}
	cui2type[cui][tp] = 1
fi.close()

print len(cui2type)

fi = open(sys.argv[2], 'r')
for line in fi:
	cui = line.strip().split('\t')[0]
	tp = line.strip().split('\t')[1]
	if cui2type.get(cui, None) == None:
		cui2type[cui] = {}
	cui2type[cui][tp] = 1
fi.close()

print len(cui2type)

# map types to the json file
fi = open(sys.argv[3], 'r')
fo = open(sys.argv[4], 'w')
cnt = 0
for line in fi:
	if cnt % 10000 == 0:
		print cnt
	cnt += 1
	dic = json.loads(line.strip())
	flag = {}
	for i in range(len(dic['entityMentions'])):
		cui = dic['entityMentions'][i]['label']
		idx = dic['entityMentions'][i]['start']
		tplst = cui2type.get(cui, {}).keys()
		if tplst != []:
			#print cui, idx, tplst
			flag[idx] = 1
			dic['entityMentions'][i]['label'] = tplst

	#print flag.keys()
	newdic = {}
	newdic["sentId"] = dic["sentId"]
	newdic["articleId"] = dic["articleId"]
	newdic["sentText"] = dic["sentText"]
	newdic["relationMentions"] = []
	newdic["entityMentions"] = []
	for i in range(len(dic['entityMentions'])):
		idx = dic['entityMentions'][i]['start']
		if idx in flag:
			newdic["entityMentions"].append(dic['entityMentions'][i])
	for i in range(len(dic['relationMentions'])):
		if dic['relationMentions'][i]["label"] == "None":
			continue
		try:
			idx1 = dic['relationMentions'][i]["em1Start"]
			idx2 = dic['relationMentions'][i]["em2Start"]
		except KeyError:
			print dic['relationMentions'][i].keys()
			exit(0)
		if flag.get(idx1, 0) == 1 and flag.get(idx2, 0) == 1:
			newdic["relationMentions"].append(dic['relationMentions'][i])
	if newdic["entityMentions"] == [] or newdic["relationMentions"] == []:
		continue
	fo.write(json.dumps(newdic) + '\n')
fi.close()
fo.close()

