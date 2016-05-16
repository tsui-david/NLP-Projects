# David Tsui 2.9.2016
# Human Languages and Technologies
# Dr. Rebecca Hwa

from Ngrams import *

#TRAIN
train_file = open("tokenized_train.txt","r")
train_str = train_file.read();
tri = Trigram(1)
print "Begin training vocabulary----------------------"
tri.trainVocabulary(train_str)
#tri.printVocabulary()

#Takes in questions for development
dev_file = open("Holmes.lm_format.questions.txt")
output_file = open("holmes_output.txt","w+")
print "Begin calculating perplexity----------------------"
for i, line in enumerate(dev_file):
	#Clean text by removing all quotations
	line = line[:-1]
	exclude = set(string.punctuation)
	s = ''.join(ch for ch in line if ch not in exclude)
	s = s.lower()
	#Lambda factors
	lu = .3
	lb = .3
	lt = .4
	print "Question %d complete" %(i)
	perplexity = tri.getPerWordPerplexityInterpolated(s,lu,lb,lt)
	newline = "%s\t%f\n"%(line,perplexity)
	output_file.write(newline)


