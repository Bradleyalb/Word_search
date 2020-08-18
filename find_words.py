def load_words():
	with open('english-words/words_alpha.txt') as word_file:
		valid_words = set(word_file.read().split())
	return valid_words


from itertools import chain, combinations

def powerset(iterable):
	"powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
	s = list(iterable)
	tmp = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
	return list(map(''.join, tmp))

def allperm(inputstr):
	for i in range(len(inputstr)):
		yield(inputstr[i])        
		for s in allperm(inputstr[:i] + inputstr[i+1:]):
			yield(inputstr[i] + s)

def find_words(letters,places):
	ewords = load_words()
	tmp = [word for word in allperm(letters) if (word in ewords and len(word) == len(places))]
	tmp = list(set(tmp))
	for index,letter in enumerate(places):
		if letter != "*":
			tmp = [word for word in tmp if word[index] == letter]
	return sorted(tmp,key = lambda k: -len(k))

for word in find_words("cmotsi","*****"):
	print(word)

	