import re
import json
import nltk

pronoun_list = ['i', 'my', 'me', 'we', 'mine', 'you', 'your', 'it', 'its', 'he', 'she', 'her', 'hers', 'his', 'our', 'us', 'ours', 'they', 'their', 'theirs']
preposition_list = ['a', 'the', 'there', 'of', 'to', 'from', 'in', 'on', 'about', 'up', 'down', 'with', 'out', 'above', 'after', 'against', 
'along', 'around', 'as', 'at', 'by', 'however', 'amid', 'before', 'behind', 'besides', 'beside', 'despite', 'except', 'during', 'include', 
'beyond', 'between', 'into', 'like', 'off', 'onto', 'over', 'per', 'plus', 'over', 'since', 'than', 'through', 'toward', 'towards', 'until', 'under', 'upon', 
'versus', 'via', 'within', 'without']
apos_list = ['s', 'd', 've', 'll', 'm', 't']
be_list = ['be', 'is', 'isn', 'are', 'aren', 'was', 'wasn', 'were', 'weren']
conjunction_list = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so', 'if']

# remove contiguous punctuations (e.g. "......", "...")
def removeExtraPunc(input_str):
	regex_dots = re.compile(r'\.+')
	regex_money = re.compile(r'\$+|\!+|\\+|\-+|\/+|\(+|\)+|\[+|\]+|\?+|\:+|\++|\^+|\<+|\>+|\{+|\}+|\&+')

	if regex_dots.match(input_str):
		# print input_str
		input_str = ' . '
	elif regex_money.match(input_str):
		# print input_str
		input_str = ''
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

def removeBe(input_str):
	if input_str in be_list:
		# print input_str
		input_str = ''
	return input_str

def removeNumbers(input_str):
	if input_str.isdigit():
		# print input_str
		input_str = ''
	return input_str

def removeConjunction(input_str):
	if input_str in conjunction_list:
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
			# print input_str
			input_str = ''
	return input_str

def removeMultipleSpaces(input_sentence):
	input_sentence = re.sub(r' +', ' ', input_sentence)
	return input_sentence


	