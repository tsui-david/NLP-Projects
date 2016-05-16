# David Tsui 2.9.2016
# Human Languages and Technologies
# Dr. Rebecca Hwa

#A simple tokenizer class that tokenizes words based on spaces and periods --> returns a sentence with array of: <s> a b c ... </s>
import sys
import re
import nltk.data
import nltk.tokenize.punkt
import string

class Tokenizer:

	def tokenize(self,str):
		str = str.strip()
		str = str.replace(' ,',',')
		str = str.replace(',',' ,')
		period_pattern = re.compile('([a-z1-9 ,]+)\. ([a-z1-9 ,]+)')
		period_pattern2 = re.compile('([a-z1-9 ,]+)\.')

		p1 = re.findall(period_pattern,str)
		for parse in p1:
			sub1 = "<s> "+parse[0]+" </s>"
			sub2 = " <s> "+parse[1]
			str = period_pattern.sub(sub1+sub2,str,1)

		p2 = re.findall(period_pattern2,str)
		for parse in p2:
			sub = "<s> "+parse+" </s>"
			str = period_pattern2.sub(sub,str,1)
		return str

	def tokenizeAdvanced(self,str):
		#STRIPS ALL PUNCTUATIONS
		str = str.strip()
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		sent_tokenize_list = sent_detector.tokenize(str)
		exclude = set(string.punctuation)
		str_all = ''
		for s in sent_tokenize_list:

			s = ''.join(ch for ch in s if ch not in exclude)
			s = s.lower()
			#ADD BEGINNING AND END
			st = "<s> %s </s> " % (s)
			str_all = "%s %s" %(str_all,st)

		return str_all




