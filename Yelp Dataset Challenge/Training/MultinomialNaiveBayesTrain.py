import re
import json
from TrainParser import *

TEST_PATH = "../../../YelpData/testAnswers.json"
CATEGORY_PATH = "../../../YelpData/category.json"
PREDICTION_OUTPUT_PATH = "../../../YelpData/prediction.json"

bdoc = open(BUSINESS_PATH)
cdoc = open(CATEGORY_PATH)
opdoc = open(PREDICTION_OUTPUT_PATH,"w+")

V = 0
alpha = 1 #Laplacian
threshold = 0.5
#Parse json files
cdict = {}
for line in cdoc:
    c = json.loads(line)
    cName = c['Category']
    cTF = c['Term Frequencies']
    cNum = c['Num Words']
    V += cNum
    if cName not in cdict:
        newCat = CategoryObj(cName,cNum,cTF)
        cdict[cName] = newCat
    else:
        print "Error extra business id %s" % bid
        break

#Add in test files to begin prediction
testDict = {}
for line in bdoc:
    b = json.loads(line)
    bTF = b['Term Frequencies']
    bID = b['ID']

    predictDict = {}
    #Calculate predictions
    sumCatProb = 0.0
    for category in cdict:
        prob = 0
        catObj = cdict[category]
        sumProb = 0.0

        for word in bTF:
            sumWordTF = catObj.getTF(word)+alpha
            allTF = catObj.numWords+alpha*V
            currWordProb = sumWordTF/allTF
            sumProb += -math.log(currWordProb,2)*(bTF[word])    #Accounts for repetition of the word

        sumCatProb += sumProb
        predictDict[category] = sumProb
    #Go through and find threshold
    
