import re
import json
import nltk

pronoun_list = ['i', 'my', 'me', 'we', 'mine', 'you', 'your', 'he', 'she', 'her', 'hers', 'his', 'our', 'us', 'ours', 'they', 'their', 'theirs']
preposition_list = ['a', 'the', 'there', 'for', 'of', 'to', 'from', 'in', 'on', 'about', 'up', 'down', 'with', 'out', 'above', 'after', 'against', 
'along', 'around', 'as', 'at', 'by', 'but', 'yet', 'however', 'amid', 'before', 'behind', 'besides', 'beside', 'despite', 'except', 'during', 'include', 
'beyond', 'between', 'into', 'like', 'off', 'onto', 'over', 'per', 'plus', 'over', 'since', 'than', 'through', 'toward', 'towards', 'until', 'under', 'upon', 
'versus', 'via', 'within', 'without']
apos_list = ['s', 'd', 've', 'll', 'm']

# remove contiguous punctuations (e.g. "......", "...")
def removeExtraPunc(input_str):
	regex_dots = re.compile(r'\.+')
	regex_ex = re.compile(r'!+')

	if regex_dots.match(input_str):
		input_str = ' . '
	elif regex_ex.match(input_str):
		input_str = ' ! '
	return input_str

def removePronouns(input_str, bool):
	if bool==False:
		return input_str
	else:
		if input_str in pronoun_list:
			# print input_str
			input_str = ''
	return input_str

def removePrepositions(input_str):
	if input_str in preposition_list:
		# print input_str
		input_str = ''
	return input_str

def removeApostrophe(input_str, bool):
	if bool==False:
		return input_str
	else:
		regex_apos = re.compile(r"'")
		if regex_apos.match(input_str):
			input_str = ''
	return input_str

def removePostfixApos(input_str, bool):
	if bool==False:
		return input_str
	else:
		if input_str in apos_list:
			print input_str
			input_str = ''
	return input_str

def removeMultipleSpaces(input_sentence):
	input_sentence = re.sub(r' +', ' ', input_sentence)
	return input_sentence


	