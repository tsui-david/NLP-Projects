# David Tsui 2.9.2016
# Human Languages and Technologies
# Dr. Rebecca Hwa

#Main program for running the part 2
#Outputs the perplexities of files in part2_output.txt
from Ngrams import *
import sys


if len(sys.argv)==5:
	ngramModel = sys.argv[1]
	trainFileStr = sys.argv[2]
	devFileStr = sys.argv[3]
	testFileStr = sys.argv[4]
	print "Model: %s Training File: %s Development File: %s Test File: %s" %(ngramModel,trainFileStr,devFileStr,testFileStr)
	print "--------------------------------------------------------------"

	pass
else:
	print("Not enough arguments")
	sys.exit()

#MAIN
train_file = open(trainFileStr,"r")
dev_file = open(devFileStr,"r")
test_file = open(testFileStr,"r")

ngram = Unigram(1)
isSmooth = False
#Select Model
if ngramModel == '1':
	pass
elif ngramModel == '2':
	ngram = Bigram(1)
elif ngramModel == '2s':
	ngram = Bigram(1)
	isSmooth = True
elif ngramModel == '3':
	ngram = Trigram(1)
elif ngramModel == '3s':
	ngram = Trigram(1)
	isSmooth = True
else:
	print "Invalid ngram model!"
	sys.exit()


t = Tokenizer()
#train_str = example.read()
train_str = train_file.read();
train_str = t.tokenize(train_str)

print "---------------------"
print "Input training string"
print "---------------------"
print train_str

print "------------------------"
print "Input development string"
print "------------------------"

dev_str = dev_file.read()
print dev_str

print "-----------------"
print "Input test string"
print "-----------------"

test_str = test_file.read()
print test_str

print "-------"
print "Results"
print "-------"


ngram.trainVocabulary(train_str)

#Reset opening the file
dev_file = open(devFileStr,"r")
test_file = open(testFileStr,"r")
output_file = open("part2_output.txt","w+")
if ngramModel == '3s':
	lu = .5
	lb = .25
	lt = .25
else:
	lu = .6
	lb = .4


print "Dev file results:"
output_file.write("Devlopment file results:\n")
for i, line in enumerate(dev_file):
	#Clean text by removing all quotations
	line = line[:-1]
	#Lambda factors

	if ngramModel == '3s':
		perplexity = ngram.getPerWordPerplexityInterpolated(line,lu,lb,lt)
	elif ngramModel == '2s':
		perplexity = ngram.getPerWordPerplexityInterpolated(line,lu,lb)
	else:
		perplexity = ngram.getPerWordPerplexity(line)

	newline = "%s\t%f\n"%(line,perplexity)
	output_file.write(newline)
	print newline

print "Test file results:"
output_file.write("\nTest file results:\n")
for i, line in enumerate(test_file):
	#Clean text by removing all quotations
	line = line[:-1]
	#Lambda factors

	if ngramModel == '3s':
		perplexity = ngram.getPerWordPerplexityInterpolated(line,lu,lb,lt)
	elif ngramModel == '2s':
		perplexity = ngram.getPerWordPerplexityInterpolated(line,lu,lb)
	else:
		perplexity = ngram.getPerWordPerplexity(line)

	newline = "%s\t%f\n"%(line,perplexity)
	output_file.write(newline)
	print newline


