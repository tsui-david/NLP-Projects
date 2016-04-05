import re
import json
import nltk

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
		regex_pronouns = re.compile(r'i|my|me|mine|you|yours|he|she|hers|his|her|our|us|ours|they|their|theirs')
		if regex_pronouns.match(input_str):
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
		regex_post = re.compile(r's|d|ve|ll|m')
		if regex_post.match(input_str):
			input_str = ''
	return input_str

def removeMultipleSpaces(input_sentence):
	input_sentence = re.sub(r' +', ' ', input_sentence)
	return input_sentence