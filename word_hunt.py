import random
import sys
import pandas as pd
import xlsxwriter
import json
from trie import Trie
#User Changed Variables
############################
depth = 8
repeat_num = 0
vowel_multiplier = 1
path = 'www'
path = "C:\\MIT\\Independent_projects\\word_search\\scrabble_words.txt"
write = True
############################

def load_words():
	with open(path) as word_file:
		valid_words = set(word_file.read().split())
	return valid_words

def build_trie(words):
	word_trie = Trie()
	for word in words:
		word_trie[word] = 1
	return word_trie
letter_freq = {'E':11.16*vowel_multiplier, 'A':8.4966*vowel_multiplier,'R':7.5809,'I':7.5448*vowel_multiplier,'O':7.1635*vowel_multiplier,'T':6.9509,
'N':6.6544,'S':5.7351,'L':5.4893,'C':4.54893,'U':3.6308*vowel_multiplier,'D':3.3844,'P':3.1671,
'M':3.0129,'H':3.0034,'G':2.4705,'B':2.0720,'F':1.8121,'Y':1.7779,'W':1.2899,
'K':1.1016,'V':1.0074,'X':0.2902,'Z':0.2722,'J':0.1965,'Q':0.1962}

total_prob = sum([letter_freq[letter] for letter in letter_freq])
def pretty_print(letter_list):
	print('-----------------')
	for i in range(0,16,4):
		print('|',letter_list[i+0],'|',letter_list[i+1],'|',letter_list[i+2],'|',letter_list[i+3],'|')
		print('-----------------')

def get(loc,letter_list):
	x,y = loc
	if x+4*y >15 or x+4*y < 0:
		print(x+4*y)
		return ""
	else:
		return letter_list[x+4*y]

def create_ll():
	ll = []
	for i in range(16):
		rand_num = random.random()*(total_prob+0.001)
		total = 0
		for letter in letter_freq:
			total+=letter_freq[letter]
			if rand_num < total:
				ll.append(letter)
				break
		if rand_num >= total:
			ll.append('E')
	#pretty_print(ll)
	return ll


def get_neighbors(loc):
	x,y = loc
	neighbors = []
	if x > 0:
		neighbors.append((x-1,y))
	if x < 3: 
		neighbors.append((x+1,y))
	if y > 0:
		neighbors.append((x,y-1))
	if y < 3:
		neighbors.append((x,y+1))
	if x<3 and y<3:
		neighbors.append((x+1,y+1))
	if x>0 and y>0:
		neighbors.append((x-1,y-1))
	if x>0 and y<3:
		neighbors.append((x-1,y+1))
	if x<3 and y>0:
		neighbors.append((x+1,y-1))
	return neighbors

all_words = load_words()
all_locations = []
for x in range(4):
	for y in range(4):
		all_locations.append((x,y))
test = build_trie(load_words())

#print("URINE" in test)
#print("URINE" in all_words)
def search_list(loc,string,letter_list,depth,visited,word_trie):
	
	cur_string = string + get((loc),letter_list)
	#print(string)
	if cur_string[0] == 'N':
		pass
		#print(cur_string)
		#print(cur_string.lower() in word_trie)
	if depth == 0 or loc in visited or not cur_string in word_trie and cur_string != "":
		#print("return")
		return set()
	words = set()
	visited.add(loc)
	for neighbor in get_neighbors(loc):
		child_words = search_list(neighbor,cur_string,letter_list,depth-1,visited,word_trie)
		if child_words:
			words = words|child_words

	if cur_string in all_words and len(cur_string) > 2: words.add(cur_string)
	visited.remove(loc)
	return words

def find_all_words(letter_list):
	words_found = set()
	for loc in all_locations:
		words = search_list(loc,"",letter_list,depth,set(),test)
		words_found = words_found|words
	return words_found
#pretty_print("ABCDEFGHIJKLMNOP")
print(find_all_words("NERLEMOATTNCHHRA"))

toolbar_width = 10

# setup toolbar
writer = pd.ExcelWriter("Word_Frequencies.xlsx",engine = 'xlsxwriter')
len_word_dic = {i:{} for i in range(depth+1)}
for i in range(repeat_num):
	if i % 100 == 0:
		print()
		print(i/100, " out of ", int(repeat_num/100))
		sys.stdout.write("[%s]" % (" " * toolbar_width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (toolbar_width+1))
	if i % 10 == 0:
		sys.stdout.write("-")
		sys.stdout.flush()
	words = find_all_words(create_ll())
	for word in words:
		if word in len_word_dic[len(word)]:
			len_word_dic[len(word)][word]["count"] += 1
			len_word_dic[len(word)][word]["maps"].append(i)
		else:
			len_word_dic[len(word)][word] = {"count": 1, "maps": [i]}
print(len_word_dic)
if write:
	json = json.dumps(len_word_dic)
	f = open("len_word_dic.json","w")
	f.write(json)
	f.close()

print()
print(len_word_dic)




	




