import random
import sys
import pandas as pd
import xlsxwriter
import json

depth = 8
with open('len_word_dic.json') as json_file:
    len_word_dic = json.load(json_file)
writer = pd.ExcelWriter("Word_Frequencies.xlsx",engine = 'xlsxwriter')
total_ranges = [(0,2),(0,3),(-2,None),(-3,None)]

def partition(i,sort_words,ranges):
	pre_dic = {}
	pre_to_words = {}
	for word in sort_words:
		pre = word[ranges[0]:ranges[1]]
		if pre in pre_dic:
			pre_dic[pre] += len_word_dic[i][word]["count"]
			pre_to_words[pre].append(word)
		else:
			pre_dic[pre] = len_word_dic[i][word]["count"]
			pre_to_words[pre] = [word]
	return pre_dic,pre_to_words

def prefixes(i,pre_dic,pre_to_words):
	pre_words = []
	sort_pre = sorted(pre_dic,key = lambda k :-pre_dic[k])[:1000]
	count_pre = []
	for pre in sort_pre:
		pre_words.append(sorted(pre_to_words[pre], key = lambda k: -len_word_dic[i][k]["count"]))
		count_set = set()
		for word in pre_to_words[pre]:
			count_set = count_set|set(len_word_dic[i][word]["maps"])
		count_pre.append(len(count_set)/100)
	return pre_words, count_pre


for i in range(depth+1):
	i = str(i)
	if len_word_dic[i] != {}:
		sort_words = sorted(len_word_dic[i], key = lambda word :-len_word_dic[i][word]["count"])[:1000]
		total_words = sum(len_word_dic[i][word]["count"] for word in len_word_dic[i])
		freq = []
		for word in sort_words:
			freq.append(len_word_dic[i][word]["count"]/100)
		df = pd.DataFrame({"Word":sort_words,"Percent Frequency":freq})
		df.to_excel(writer, sheet_name = "Words of length {}".format(i),index = False)
		for ranges in total_ranges:
			pre_dic, pre_to_words = partition(i,sort_words,ranges)
			sort_pre = sorted(pre_dic,key = lambda k :-pre_dic[k])[:1000]
			pre_words,count_pre = prefixes(i,pre_dic,pre_to_words)
			df = pd.DataFrame({"Common Prefix": sort_pre, "Percentage": count_pre, "Assoicated Words": pre_words})
			df.to_excel(writer, sheet_name = "{} of length {}".format(ranges,i),index = False)
writer.save()