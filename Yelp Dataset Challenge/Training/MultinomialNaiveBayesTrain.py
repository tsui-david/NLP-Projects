import re
import json
import math
import operator
from TrainParser import *

TEST_PATH = "../../../YelpData/testAnswers.json"
CATEGORY_PATH = "../../../YelpData/category.json"
PREDICTION_OUTPUT_PATH = "../../../YelpData/prediction.json"

tdoc = open(TEST_PATH)
cdoc = open(CATEGORY_PATH)
opdoc = open(PREDICTION_OUTPUT_PATH,"w+")

V = 0
alpha = .001 #Laplacian
threshold = 0.0021
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
size =  len(tdoc.readlines())
tdoc.seek(0,0)
currLine = 0
testDict = []
for line in tdoc:
    currLine += 1

    b = json.loads(line)
    bTF = b['Term Frequencies']
    bID = b['ID']

    predictions = []
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

            if currWordProb == 0.0:
                sumProb += 0.0
            else:
                sumProb += -math.log(currWordProb,2)*(bTF[word])    #Accounts for repetition of the word

        sumCatProb += sumProb
        predictDict[category] = sumProb

    #predictions.append(maximum)
    for cat in predictDict:
        sumProb = predictDict[cat]
        allProb = sumProb/sumCatProb
        if allProb >= threshold:
            predictions.append(cat)

    if(len(predictions) == 0):
        maximum = max(predictDict, key=predictDict.get)
        predictions.append(maximum)


    bObj = BusinessObj(bID,predictions)
    testDict.append(bObj)
    print("%d out of %d completed") % (currLine,size)
opdoc.seek(0,0)
for business in testDict:
    opdoc.write(business.toJSONMachine()+'\n')
