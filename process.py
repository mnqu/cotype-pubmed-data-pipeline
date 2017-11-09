import sys
import os
import json

def read_sentences(file_name):
	sentences = []
	fi = open(file_name, 'r')
	sent = []
	for line in fi:
		if line == '\n':
			sentences.append(sent)
			sent = []
			continue
		word = line.strip().split('\t')[0]
		ner = line.strip().split('\t')[1]
		sent.append([word, ner])
	return sentences

def get_entity(sentence):
	entity_list = []
	last_ner = 'O'
	bg, ed, pst = -1, -1, 0
	for entry in sentence:
		word = entry[0]
		ner = entry[1]
		if ner != last_ner:
			if last_ner == 'O':
				p = pst
			else:
				q = pst
				entity_list.append((p, q, last_ner))
		last_ner = ner
		pst += 1
	return entity_list

def get_name(sentence, p, q):
	text = ''
	for k in range(p, q):
		text += sentence[k][0] + ' '
	return text.strip()

def get_name2cui(name2cui_umls, name2cui_go):
	name2flag = {}
	name2cui = {}

	fi = open(name2cui_umls, 'r')
	for line in fi:
		lst = line.strip().split('\t')
		name = lst[0].lower()
		cui = lst[1]

		name2flag[name] = 1
		name2cui[name] = cui
	fi.close()

	fi = open(name2cui_go, 'r')
	for line in fi:
		lst = line.strip().split()
		name = lst[0]
		cui = lst[1]

		name2flag[name] = 2
		name2cui[name] = cui
	fi.close()

	return name2flag, name2cui

def get_cui2type(cui2type_umls, cui2type_go):
	cui2type = {}
	fi = open(cui2type_umls, 'r')
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

	fi = open(cui2type_go, 'r')
	for line in fi:
		cui = line.strip().split('\t')[0]
		tp = line.strip().split('\t')[1]
		if cui2type.get(cui, None) == None:
			cui2type[cui] = {}
		cui2type[cui][tp] = 1
	fi.close()

	return cui2type

def get_pair2relation(file_name):
	pair2flag = {}
	pair2relation = {}

	fi = open(file_name, 'r')
	for line in fi:
		lst = line.strip().split('\t')
		cui1 = lst[1]
		cui2 = lst[0]
		rlt = lst[2]

		pair2flag[(cui1, cui2)] = 1
		if pair2relation.get((cui1, cui2), None) == None:
			pair2relation[(cui1, cui2)] = {}
		pair2relation[(cui1, cui2)][rlt] = 1
	fi.close()

	return pair2flag, pair2relation

ner_text_file = sys.argv[1]
name2cui_umls_file = sys.argv[2]
name2cui_go_file = sys.argv[3]
cui2type_umls_file = sys.argv[4]
cui2type_go_file = sys.argv[5]
pair2relation_file = sys.argv[6]
output_file = sys.argv[7]

sentences = read_sentences(ner_text_file)
name2flag, name2cui = get_name2cui(name2cui_umls_file, name2cui_go_file)
pair2flag, pair2relation = get_pair2relation(pair2relation_file)
cui2type = get_cui2type(cui2type_umls_file, cui2type_go_file)

sent_id = 0
fo = open(output_file, 'w')
for sent in sentences:
	
	ent_list = get_entity(sent)

	valid_ent_list = []
	for ent in ent_list:
		name = get_name(sent, ent[0], ent[1])
		if name2flag.get(name, 0) != 0:
			cui = name2cui[name]
			types = cui2type.get(cui, {}).keys()
			if len(types) == 1:
				valid_ent_list.append([cui, name, types[0], ent[0], ent[1]])

	if len(valid_ent_list) < 2:
		continue

	relation_list = []

	for u in range(len(valid_ent_list)):
		for v in range(len(valid_ent_list)):
			if u == v:
				continue
			entu = valid_ent_list[u]
			entv = valid_ent_list[v]

			cuiu = entu[0]
			cuiv = entv[0]

			if cuiu == cuiv:
				continue

			rels = []
			if pair2flag.get((cuiu, cuiv), 0) == 1:
				rels = pair2relation[(cuiu, cuiv)].keys()

			if len(rels) == 1:
				rel = rels[0]
				relation_list.append([entu, entv, rel])

	if len(relation_list) == 0:
		continue

	dic = {}
	dic["sentText"] = get_name(sent, 0, len(sent))
	dic["articleId"] = sent_id
	dic["sentId"] = sent_id
	dic["entityMentions"] = []
	for ent in valid_ent_list:
		edic = {}
		edic["text"] = ent[1]
		edic["start"] = ent[3] #edic["start"] = ent[1]
		edic["label"] = ent[2]
		dic["entityMentions"].append(edic)
	dic["relationMentions"] = []
	for rel in relation_list:
		#print rel
		rdic = {}
		rdic["em1Text"] = rel[0][1]
		rdic["em2Text"] = rel[1][1]
		rdic["em1Start"] = rel[0][3] 
		rdic["em2Start"] = rel[1][3]
		rdic["label"] = rel[2]
		dic["relationMentions"].append(rdic)
	sent_id += 1

	fo.write(json.dumps(dic) + '\n')
fo.close()
