# David Tsui 2.9.2016
# Human Languages and Technologies
# Dr. Rebecca Hwa

# Ngram that spans from unigram to trigram with good turing smoothing implementation
# Implementation:
# 	Add new vocabulary to dictionary and compute conditional probabilities given past vocabularies
#	Account for smoothing using good turing algorithm: [Frequency of count+1 * (count+1)]/Frequency of current count
from Tokenizer import *
import math

class Ngram:
	#0.0 to initalize as floats
	total_count = 0.0
	vocab = {}
	corpus = [""]
	K = 1
	unknown_count = 0.0
	num_sentences = 0.0

	#@param args:
	# v -- lexicon V for threshold of <unknown> replacement -- default should be 1
	def __init__(self,K):

		self.K = K

	def processUnknown(self):

		for word in self.vocab:
			#Remove vocab and add to unknow if less than k
			if self.vocab[word] <= self.K and word != '<s>' and word !='</s>':
				self.unknown_count += self.vocab[word]
				self.vocab[word] = -1

	#Prints the dictionary for testing purposes
	def printVocabulary(self):
		print "-------------------Unigram----------------------------"
		print "Total count: %d" % (self.total_count)
		for word in self.vocab:
			print "%s\tC: %d\tP: %f" % (word, self.vocab[word], self.getP(word))

		print "<Unknown> : %f" % self.getP("<Unknown>")

	#Get unknown
	def getUnknownCount(self):
		return self.unknown_count

	def getSentenceEntropy(self,sentence):

		words = sentence.split(" ")
		sum_prob = 0.0
		for word in words:
			if word != "<s>":
				print "%s %f " % (word,self.getP(word))
				sum_prob += -1*math.log(self.getP(word),2)
#		print "sum_prob: " %(sum_prob)
		return sum_prob

	def calculatePerWordPerplexity(self,sentence):
#		print "%s ~~~" %(sentence[:-1])
		words = sentence.split(" ")
		l = len(words)-1
		entropy = self.getSentenceEntropy(sentence)

		if entropy == -1:
			return float("inf")
		entropy_per_word = entropy/l
#		print(entropy_per_word)
		perplexity_per_word = math.pow(2,entropy_per_word)

		return perplexity_per_word

	def printPerWordPerplexity(self,file):
		t = Tokenizer()
		print "---------------Perplexity Per Word-----------------------"

		for line in file:
			line = t.tokenize(line)
			perplexity = self.calculatePerWordPerplexity(line)
			print "%s:\t%f" % (line,perplexity)

	def getPerWordPerplexity(self,line):
		t = Tokenizer()
		line = t.tokenize(line)
		perplexity = self.calculatePerWordPerplexity(line)
		return -perplexity

#-----------------------------UNIGRAM----------------------------------------------

#Class for unigram that accounts for <Unknown>
class Unigram(Ngram):
	#0.0 to initalize as floats
	total_count = 0.0
	vocab = {}
	corpus = [""]
	K = 1.0
	unknown_count = 0.0

	#@param args:
	# v -- lexicon V for threshold of <unknown> replacement -- default should be 1
	def __init__(self,K):

		self.K = K
		#Get the probability
	def getP(self,word):
		if word == "<s>":
			return 1
		elif word in self.vocab and self.vocab[word] > self.K:
			return (self.vocab[word]/self.total_count)
		else:
			return self.unknown_count/self.total_count

	#@param args:
	# train_file -- file for training vocabulary
	# return the vocabulary dictionary
	def trainVocabulary(self,train_str):

		self.corpus = train_str.split()

		self.total_count = len(self.corpus)

		for word in self.corpus:

			if word in self.vocab:
				self.vocab[word] = self.vocab[word]+1.0
			else:
				v = {word:1.0}
				self.vocab.update(v)
		self.total_count -= self.vocab['<s>']
		self.processUnknown()
		return self.vocab

#-------------------------Bigram---------------------------------
class Bigram(Ngram):

	corpus = [""]
	total_count = 0
	#Holds the bigram dictionary <key>: previous word, current word, <value>: count of previous word, current word
	bigram_dict = {}
	#Holds the unigram dictionary <key>: current word, <value>: count of current word
	vocab = {}

	K = 1.0
	unknown_count = 0.0
	previous_word = "<s>"

	def __init__(self,k):

		self.K = k

	#Sets the unigram dictionary if it has already been calcualted
	def setDictionary(self,unigram_dict,unknown_count):
		self.vocab = unigram_dict

	#Add vocabulary into dictionary, replace k threshold words with unknown by calling processUnknown()
	#Returns the trained bigram dictionary
	def trainVocabulary(self,train_str):

		self.corpus = train_str.split()
		self.total_count = len(self.corpus)

		#Makes sure that there is no dictionary before making a dictionary
		if len(self.vocab)==0:

			self.corpus = train_str.split()

			self.total_count = len(self.corpus)

			for word in self.corpus:

				if word in self.vocab:
					self.vocab[word] = self.vocab[word]+1.0
				else:
					v = {word:1.0}
					self.vocab.update(v)
		self.total_count -= self.vocab['<s>']
		self.processUnknown()

		for word in self.corpus:

			if self.vocab[word] == -1:
				word = '<Unknown>'
			if (self.previous_word,word) in self.bigram_dict:
				if word == '<s>':
					previous_word = '<s>'
				self.bigram_dict[(self.previous_word,word)] = self.bigram_dict[(self.previous_word,word)]+1.0
				self.previous_word = word

			else:
				if word == '<s>':
					self.previous_word = '<s>'
				v = {(self.previous_word,word):1.0}
				self.bigram_dict.update(v)
				self.previous_word = word



		return self.bigram_dict

	def getUnigramP(self,word):
		if word == "<s>":
			return 1

		word_count = 0
		if word in self.vocab and self.vocab[word]>0:
			word_count = self.vocab[word]
		else:
			word_count = self.unknown_count

		return word_count/self.total_count

	#Calculates the probability of bigram with no smoothing
	def getP(self,previous_word,curr_word):
		if previous_word == "<s>" and curr_word == "<s>":
			return 1
#		print (previous_word,curr_word,self.vocab[previous_word],self.vocab[curr_word],self.unknown_count)
		if curr_word in self.vocab and self.vocab[curr_word]>0:
			pass
		else:
			curr_word = "<Unknown>"

		if previous_word in self.vocab and self.vocab[previous_word]>0:
			pass
		else:
			previous_word = "<Unknown>"
		#Count of previous word AND current word

		#Count of previous word
		if previous_word == "<Unknown>":
			c_prev = self.unknown_count
		else:
			c_prev = self.vocab[previous_word]



		bigram_words = (previous_word,curr_word)

		#Ensures that the words are in dictionary else return infinity
#		print bigram_words
		if bigram_words in self.bigram_dict and c_prev > 0:

			c_bigram = self.bigram_dict[(previous_word,curr_word)]
#			print "Current: %s, Previous: %s, Count of bigram: %d, Count of previous: %d" %(bigram_words[1],bigram_words[0],c_bigram,c_prev)
			return c_bigram/c_prev

		else:
			return float("-inf")

	def getSentenceEntropy(self,sentence):
		words = sentence.split(" ")
		sum_prob = 0.0
		previous = "<s>"
		for word in words:
			if(word!=""):
				current = word
				#print "%s -- %f -- " % (word,-1*math.log(self.getP(previous,current),2))
				probability = self.getP(previous,current)
				print "%s --> %s %f"%(previous,current,probability)
				if probability == float("-inf"):
					return -1
				else:
					sum_prob += -1*math.log(probability,2)
					previous = current
	#				print "sum_prob: " %(sum_prob)
		return sum_prob

	def getSentenceEntropyInterpolated(self,sentence,lu,lb):

		words = sentence.split(" ")
		sum_prob = 0.0
		previous = "<s>"
		for word in words:
			if(word!=""):
				current = word
				#print "%s -- %f -- " % (word,-1*math.log(self.getP(previous,current),2))
				biP = self.getP(previous,current)

				uniP = self.getUnigramP(current)
				if biP == float("-inf"):
					biP = 0
				probability = (lu*uniP)+(lb*biP)

				if probability == 0:
					return float("-inf")
				else:
					print "%s --> %s %f"%(previous,current,probability)
					sum_prob += -1*math.log(probability,2)
					previous = current

#		print "lambdau: %f, lambdabi: %f, bigram_p: %f, unigram_p: %f" %(lambda_unigram,lambda_bigram,bigram_p,unigram_p)
		return sum_prob

	def calculatePerWordPerplexityInterpolated(self,sentence,lu,lb):

		words = sentence.split(" ")
		l = len(words)-1
		entropy = self.getSentenceEntropyInterpolated(sentence,lu,lb)
		if entropy == float("-inf"):
			return float("inf")
		entropy_per_word = entropy/l

		perplexity_per_word = math.pow(2,entropy_per_word)
		return perplexity_per_word

	#Prints the dictionary for testing purposes
	def printVocabulary(self):
		print("\n-----------BIGRAM------------\n")
		for word in self.bigram_dict:
			print "%s --> %s:\tC: %d\tP: %f" % (word[0], word[1],self.bigram_dict[word[0],word[1]], self.getP(word[0],word[1]))
		print "-------------------Unigram----------------------------"
		print "Total count: %d" % (self.total_count)
		for word in self.vocab:
			print "%s\tC: %d\tP: %f" % (word, self.vocab[word], self.getUnigramP(word))

		print "<Unknown>: %f" % (self.getUnigramP("<Unknown>"))

	def printPerWordPerplexityInterpolated(self,file,lambda_uni,lambda_bi):
		t = Tokenizer()
		print "---------------Perplexity Per Word-----------------------"

		for line in file:
			line = t.tokenize(line)
			perplexity = self.calculatePerWordPerplexityInterpolated(line,lambda_uni,lambda_bi)
			print "%s:\t%f" % (line,perplexity)

	def getPerWordPerplexityInterpolated(self,line,lu,lb):
		perplexity = self.calculatePerWordPerplexityInterpolated(line,lu,lb)
		return -perplexity

class Trigram(Ngram):

	corpus = [""]
	total_count = 0
	#Holds the trigram dictionary <key>: previous previous word,previous word, current word, <value>: count of previous word, current word
	bigram_dict = {}
	trigram_dict = {}
	#Holds the unigram dictionary <key>: current word, <value>: count of current word
	vocab = {}

	K = 1.0
	unknown_count = 0.0
	pre_previous_word = "<s>"
	previous_word = "<s>"

	def __init__(self,k):

		self.K = k

	#Set unigram and bigram dictionaries if the dictionaries have already been calculated
	def setDictionaries(unigram_dict,bigram_dict,unknown_count):

		self.bigram_dict = bigram_dict
		self.vocab = unigram_dict

	#Add vocabulary into dictionary, replace k threshold words with unknown by calling processUnknown()
	def trainVocabulary(self,train_str):

		self.corpus = train_str.split()
		self.total_count = len(self.corpus)

		#Unigram training
		for word in self.corpus:

			if word in self.vocab:
				self.vocab[word] = self.vocab[word]+1.0
			else:
				v = {word:1.0}
				self.vocab.update(v)
		self.total_count -= self.vocab['<s>']
		self.processUnknown()
		#Bigram training
		for word in self.corpus:
			if word == '<s>':
				self.previous_word = '<s>'
			if self.vocab[word] == -1:
				word = '<Unknown>'
			if (self.previous_word,word) in self.bigram_dict:

				self.bigram_dict[(self.previous_word,word)] = self.bigram_dict[(self.previous_word,word)]+1.0
				self.previous_word = word
				if word == '</s>':
					previous_word = "<s>"
			else:
				v = {(self.previous_word,word):1.0}
				self.bigram_dict.update(v)
				self.previous_word = word
				if word == '</s>':
					previous_word = "<s>"
		#Trigram training
		for word in self.corpus:
			if word == '<s>':
				self.previous_word = '<s>'
				self.pre_previous_word = '<s>'
			if self.vocab[word] == -1:
				word = '<Unknown>'
			if (self.pre_previous_word,self.previous_word,word) in self.trigram_dict:

				self.trigram_dict[(self.pre_previous_word,self.previous_word,word)] = self.trigram_dict[(self.pre_previous_word,self.previous_word,word)]+1.0
				self.pre_previous_word = self.previous_word
				self.previous_word = word

				if word == '</s>':
					self.previous_word = "<s>"
					self.pre_previous_word = "<s>"

			#NEW SENTENCE
			else:
				v = {(self.pre_previous_word,self.previous_word,word):1.0}
				self.trigram_dict.update(v)
				self.pre_previous_word = self.previous_word
				self.previous_word = word
				if word == '</s>':
					self.previous_word = "<s>"
					self.pre_previous_word = "<s>"

		return self.trigram_dict

	def getUnigramP(self,word):
		if word == "<s>":
			return 1
		elif word in self.vocab and self.vocab[word] > self.K:
			return (self.vocab[word]/self.total_count)
		else:
			return self.unknown_count/self.total_count


	def getBigramP(self,previous_word,curr_word):
		if previous_word == "<s>" and curr_word == "<s>":
			return 1
#		print (previous_word,curr_word,self.vocab[previous_word],self.vocab[curr_word],self.unknown_count)
		if curr_word in self.vocab and self.vocab[curr_word]>0:
			pass
		else:
			curr_word = "<Unknown>"

		if previous_word in self.vocab and self.vocab[previous_word]>0:
			pass
		else:
			previous_word = "<Unknown>"
		#Count of previous word AND current word

		#Count of previous word
		if previous_word == "<Unknown>":
			c_prev = self.unknown_count
		else:
			c_prev = self.vocab[previous_word]



		bigram_words = (previous_word,curr_word)

		#Ensures that the words are in dictionary else return infinity
#		print bigram_words
		if bigram_words in self.bigram_dict and c_prev > 0:

			c_bigram = self.bigram_dict[(previous_word,curr_word)]
#			print "Current: %s, Previous: %s, Count of bigram: %d, Count of previous: %d" %(bigram_words[1],bigram_words[0],c_bigram,c_prev)
			return c_bigram/c_prev

		else:
			return float("-inf")

	#Calculates the probability of bigram with no smoothing
	def getP(self,pre_previous_word,previous_word,curr_word):
		#Replace unknown
		if(pre_previous_word == '<s>' and previous_word =='<s>' and curr_word == '<s>'):
			return 1
		if curr_word in self.vocab and self.vocab[curr_word]>self.K:
			pass
		else:
			curr_word = "<Unknown>"

		if previous_word in self.vocab and self.vocab[previous_word]>self.K:
			pass
		else:
			previous_word = "<Unknown>"

		if pre_previous_word in self.vocab and self.vocab[pre_previous_word]>self.K:
			pass
		else:
			pre_previous_word = "<Unknown>"

		trigram_words = (pre_previous_word,previous_word,curr_word)
		bigram_words = (pre_previous_word,previous_word)

		#Ensures that the words are in dictionary else return infinity
		if trigram_words in self.trigram_dict and bigram_words in self.bigram_dict:
			#Count of pre_previous AND previous word AND current word
			c_trigram = self.trigram_dict[(pre_previous_word,previous_word,curr_word)]
			#Count of pre_previous AND previous
			c_bigram = self.bigram_dict[(pre_previous_word,previous_word)]

			return c_trigram/c_bigram
		else:
			return float("-inf")

	def getSentenceEntropy(self,sentence):
		words = sentence.split(" ")
		sum_prob = 0.0
		previous = "<s>"
		pre_previous = "<s>"
		for word in words:
			if(word!=""):
				current = word
				#print "%s -- %f -- " % (word,-1*math.log(self.getP(previous,current),2))
				probability = self.getP(pre_previous,previous,current)
				print "%s --> %s --> %s: %f"%(pre_previous,previous,current,probability)
				if probability == float("-inf"):
					return -1
				else:
					sum_prob += -1*math.log(probability,2)
					pre_previous = previous
					previous = current
	#				print "sum_prob: " %(sum_prob)
		return sum_prob

	def getSentenceEntropyInterpolated(self,sentence,lu,lb,lt):

		words = sentence.split(" ")
		sum_prob = 0.0
		previous = "<s>"
		pre_previous = "<s>"
		for word in words:
			if(word!=""):
				current = word
				#print "%s -- %f -- " % (word,-1*math.log(self.getP(previous,current),2))
				triP = self.getP(pre_previous,previous,current)
				biP = self.getBigramP(previous,current)
				uniP = self.getUnigramP(current)
#				print "triP: %f, biP: %f, uniP: %f" %(triP,biP,uniP)
				if triP == float("-inf"):
					triP = 0
				if biP == float("-inf"):
					biP = 0
				probability = (lu*uniP)+(lb*biP)+(lt*triP)
				print "%s --> %s --> %s %f"%(pre_previous,previous,current,probability)
				if probability == 0:
					return float("-inf")
				else:
					sum_prob += -1*math.log(probability,2)
					pre_previous = previous
					previous = current

#		print "lambdau: %f, lambdabi: %f, bigram_p: %f, unigram_p: %f" %(lambda_unigram,lambda_bigram,bigram_p,unigram_p)
		return sum_prob

	def calculatePerWordPerplexityInterpolated(self,sentence,lu,lb,lt):

		words = sentence.split(" ")
		l = len(words)-1
		entropy = self.getSentenceEntropyInterpolated(sentence,lu,lb,lt)
		if entropy == float("-inf"):
			return float("inf")
		entropy_per_word = entropy/l

		perplexity_per_word = math.pow(2,entropy_per_word)
		return perplexity_per_word

	#Prints the dictionary for testing purposes
	def printVocabulary(self):
		print("-----------TRIGRAM-----------")
		for word in self.trigram_dict:
			print "%s --> %s --> %s:\tC:%d \tP: %f" % (word[0], word[1], word[2], self.trigram_dict[(word[0],word[1],word[2])],self.getP(word[0],word[1],word[2]))
		print("\n-----------BIGRAM------------\n")
		for word in self.bigram_dict:
			print "%s --> %s:\tC: %d\tP: %f" % (word[0], word[1],self.bigram_dict[word[0],word[1]], self.getBigramP(word[0],word[1]))
		print "-------------------Unigram----------------------------"
		print "Total count: %d" % (self.total_count)
		for word in self.vocab:
			print "%s\tC: %d\tP: %f" % (word, self.vocab[word], self.getUnigramP(word))

		print "<Unknown> : %f" % self.getUnigramP("<Unknown>")

	def printPerWordPerplexityInterpolated(self,file,lu,lb,lt):
		t = Tokenizer()
		print "---------------Perplexity Per Word-----------------------"

		pReturn = []
		for line in file:
			line = t.tokenize(line)
			perplexity = self.calculatePerWordPerplexityInterpolated(line,lu,lb,lt)
			print "%s:\t%f" % (line,perplexity)
			pReturn.append((line,perplexity))

	def getPerWordPerplexityInterpolated(self,line,lu,lb,lt):
		print "---------------Perplexity Per Word-----------------------"
		perplexity = self.calculatePerWordPerplexityInterpolated(line,lu,lb,lt)
		return -perplexity
