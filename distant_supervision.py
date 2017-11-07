import sys
import os
import json
import random

# max length of entities
max_length = 8

name2cui_file = sys.argv[1]
name2go_file = sys.argv[2]
pair2rlt_file = sys.argv[3]
text_file = sys.argv[4]
output_file = sys.argv[5]
name2stop_file = sys.argv[6]
instance_file = sys.argv[7]

# mapping name to cui
name2cui = {}
# mapping name to category, 1 for umls entity, 2 for go entity.
name2flag = {}
# mapping name pair to relation
pair2rlt = {}
# mapping name pair to flag
pair2flag = {}
# vocabulary of stop words
name2stop = {}

fi = open(name2cui_file, 'r')
for line in fi:
	lst = line.strip().split('\t')
	name = lst[0].lower()
	cui = lst[1]

	name2flag[name] = 1
	name2cui[name] = cui
fi.close()

print len(name2cui)

fi = open(name2go_file, 'r')
for line in fi:
	lst = line.strip().split()
	name = lst[0]
	cui = lst[1]

	name2flag[name] = 2
	name2cui[name] = cui
fi.close()

print len(name2cui)

fi = open(pair2rlt_file, 'r')
for line in fi:
	lst = line.strip().split('\t')
	#cui1 = lst[0]
	#cui2 = lst[1]
	cui1 = lst[1]
	cui2 = lst[0]
	rlt = lst[2]

	pair2flag[(cui1, cui2)] = 1
	if pair2rlt.get((cui1, cui2), None) == None:
		pair2rlt[(cui1, cui2)] = {}
	pair2rlt[(cui1, cui2)][rlt] = 1
fi.close()

print len(pair2rlt)

fi = open(name2stop_file, 'r')
for line in fi:
	name = line.strip()
	name2stop[name] = 1
	name2flag[name] = 0
	name2flag[name.upper()] = 0
fi.close()

print len(name2stop)

fi = open(text_file, 'r')
fo = open(output_file, 'w')
foins = open(instance_file, 'w')
cnt = 0
while True:
	# reading data
	title = fi.readline()
	line = fi.readline()
	if not title:
		break
	if not line:
		break

	if cnt % 1000 == 0:
		print cnt
	cnt += 1

	docid = int(title.split('\t')[0])
	senid = int(title.split('\t')[1])

	# use backward name matching to find entity mentions

	ent_lst = []

	word_lst = line.strip().split(' ')
	slen = len(word_lst)
	begin = 0
	end = slen

	idcnt = 0
	while True:
		if end <= 0:
			break

		begin = max(0, end - max_length)

		for p in range(begin, end):
			s = word_lst[p]
			for i in range(p + 1, end):
				s = s + ' ' + word_lst[i]

			if name2flag.get(s, 0) == 2:
				cui = name2cui[s]
				ent_lst.append((cui, p, end, s, 0, idcnt))
				idcnt += 1
				end = p
				break
			if name2flag.get(s.lower(), 0) == 1:
				cui = name2cui[s.lower()]
				ent_lst.append((cui, p, end, s.lower(), 0, idcnt))
				idcnt += 1
				end = p
				break
			if p == end - 1:
				end = p
				break

	pos_rel_lst = []
	neg_rel_lst = []

	# for each entity pair, find their relation from umls.

	for u in range(len(ent_lst)):
		for v in range(len(ent_lst)):
			if u == v:
				continue
			entu = ent_lst[u]
			entv = ent_lst[v]

			cuiu = entu[0]
			cuiv = entv[0]

			if cuiu == cuiv:
				continue

			rels = ['None']
			if pair2flag.get((cuiu, cuiv), 0) == 1:
				rels = pair2rlt[(cuiu, cuiv)].keys()

			for rel in rels:
				if rel == 'None':
					neg_rel_lst.append((entu[3], entv[3], rel, entu[1], entv[1], entu[5], entv[5]))
				else:
					pos_rel_lst.append((entu[3], entv[3], rel, entu[1], entv[1], entu[5], entv[5]))
					foins.write(cuiu + '\t' + cuiv + '\t' + rel + '\n')

	if len(ent_lst) <= 1:
		continue
	if len(pos_rel_lst) == 0:
		continue

	# output all entity pairs with relations

	dic = {}
	dic["sentText"] = line.strip()
	dic["articleId"] = docid
	dic["sentId"] = senid
	dic["entityMentions"] = []
	for ent in ent_lst:
		edic = {}
		edic["text"] = ent[3]
		edic["start"] = ent[5] #edic["start"] = ent[1]
		edic["label"] = ent[0]
		dic["entityMentions"].append(edic)
	dic["relationMentions"] = []
	for rel in pos_rel_lst:
		#print rel
		rdic = {}
		rdic["em1Text"] = rel[0]
		rdic["em2Text"] = rel[1]
		rdic["em1Start"] = rel[5] #rdic["em1Start"] = rel[3]
		rdic["em2Start"] = rel[6] #rdic["em2Start"] = rel[4]
		rdic["label"] = rel[2]
		dic["relationMentions"].append(rdic)
	#random.shuffle(neg_rel_lst)
	#max_num = len(pos_rel_lst) * 1
	#for rel in neg_rel_lst:
	#	max_num -= 1
	#	if max_num < 0:
	#		break
	#	rdic = {}
	#	rdic["em1Text"] = rel[0]
	#	rdic["em2Text"] = rel[1]
	#	rdic["em1Start"] = rel[5] #rdic["em1Start"] = rel[3]
	#	rdic["em2Start"] = rel[6] #rdic["em2Start"] = rel[4]
	#	rdic["label"] = rel[2]
	#	dic["relationMentions"].append(rdic)

	#print '---', len(ent_lst), len(pos_rel_lst), len(neg_rel_lst)
	#print dic["sentText"]
	#print ent_lst
	fo.write(json.dumps(dic) + '\n')
	#break

	#exit(0)

fi.close()
fo.close()
foins.close()




