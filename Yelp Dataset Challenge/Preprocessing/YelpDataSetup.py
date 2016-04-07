import re
import json
import nltk
from Parser import *
from Preprocess import *
from nltk.stem.porter import PorterStemmer
from nltk.metrics import edit_distance
from nltk.tokenize import wordpunct_tokenize

BUSINESS_PATH = "../../../YelpData/small_business.json"
REVIEW_PATH = "../../../YelpData/small_review.json"
OUTPUT_TEST_PATH = "../../../YelpData/testAnswers.json"
OUTPUT_CATEGORY_PATH = "../../../YelpData/category.json"

bdoc = open(BUSINESS_PATH)
rdoc = open(REVIEW_PATH)

obdoc = open(OUTPUT_TEST_PATH, "w+")
ocdoc = open(OUTPUT_CATEGORY_PATH, "w+")

#Parse business document with reviews
trainDict = {}  #Training business dictionary
testDict = {} #Testing business dicitonary
#Training/Testing partition
size =  len(rdoc.readlines())
rdoc.seek(0,0)
trainSize = size*(.9)
currSize = 0

porter_stemmer = PorterStemmer()
for line in rdoc:
#Size counts for paritioning training and testing
    currSize += 1
    b = json.loads(line)
    bkey = b['business_id']
    review = b['text']
    # review = "hi my name is.....char"
    # tokenize the sentence by white space and punctuations; prepare for stemming
    new_sent = wordpunct_tokenize(review)
    
    new_review = ''
    # stem each words in the sentence
    for w in new_sent:
        # remove recurring "." or "!"
        w = removeExtraPunc(w)
        # decapitalize each word
        w = w.lower()
        # remove pronouns
        w = removePronouns(w, True)
        # remove preposition
        w = removePrepositions(w)
        # remove apostrophe & postfix of Apostrophe
        w = removeApostrophe(w, True)
        w = removePostfixApos(w, True)

        # Stemming
        new_review += porter_stemmer.stem(w)
        new_review += " "
    # remove extra spaces
    new_review = removeMultipleSpaces(new_review)
    print "ORI: " + review + "\n"
    print "NEW: " + new_review + "\n"

    if currSize <= trainSize:

        if bkey not in trainDict:
            Bus = BusinessParser(bkey)
            trainDict[bkey] = Bus

        trainDict[bkey].addText(new_review)
    else:
        if bkey not in testDict:
            Bus = BusinessParser(bkey)
            testDict[bkey] = Bus

        testDict[bkey].addText(new_review)

#Parse categories with businesses
cdict = {}
for line in bdoc:
    b = json.loads(line)
    bkey = b['business_id']
    categories = b['categories']
    if bkey in trainDict:
        bobj = trainDict[bkey]
        words = bobj.dictionary
        numWords = bobj.numWords
        for category in categories:
            if category not in cdict:
                Cat = CategoryParser(category)
                cdict[category] = Cat


            cdict[category].addBusiness(bkey)
            cdict[category].updateReview(words,numWords)

    elif bkey in testDict:
        bobj = testDict[bkey]
        bobj.addCategory(categories)

#Overwrite all previous file data
# obdoc.seek(0,0)
# for bkey in bdict:
#     obdoc.write(bdict[bkey].toJSONMachine()+'\n')
obdoc.seek(0,0)
for bkey in testDict:
    obdoc.write(testDict[bkey].toJSONMachine()+'\n')
ocdoc.seek(0,0)
for ckey in cdict:
    ocdoc.write(cdict[ckey].toJSONMachine()+'\n')
