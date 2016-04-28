## This python script is a classifier that takes in trained histogram of words per categories. Using the trained histograms per categories
## It computes the argmax of the reviews of the business given its most likeley categories
import re
import json
import math
import operator
from TrainParser import *

class Naive_Bayes_Category_Classifier:
    def __init__(self,TRAINING_PATH,TEST_PATH,OUTPUT_PATH):
        PREDICTION_OUTPUT_PATH = OUTPUT_PATH+"prediction.txt"
        ## Files
        test_doc = open(TEST_PATH)
        train_doc = open(TRAINING_PATH)
        opdoc = open(PREDICTION_OUTPUT_PATH,"w+")

        V = 0
        alpha = .5 #Smoothing value for 0 occurences (1 == Laplacian)
        threshold = 0.5

        ## -- CLASSIFIER SETUP --
        cdict = {}
        for line in train_doc:
            c = json.loads(line)
            cName = c['Category']
            cTF = c['Term Frequencies']
            cNum = c['Num Words']
            V += cNum
            if cName not in cdict:
                newCat = CategoryObj(cName,cNum,cTF)
                cdict[cName] = newCat
            else:
                print "Error can't have extra categories in a set!"+" Category: "+cName
                break

        ## -- PREDICTION SETUP --
        size =  len(train_doc.readlines())
        train_doc.seek(0,0)
        currLine = 0
        testDict = []
        for line in test_doc:
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

        ## -- WRITE OUT PREDICTIONS --
        opdoc.seek(0,0)
        for business in testDict:
            opdoc.write(business.toJSONMachine()+'\n')

training_path = "../../../YelpData/SplitFiles/Split1/naiveBayesTrain.txt"
testing_path = "../../../YelpData/SplitFiles/Split1/naiveBayesTest.txt"
output_path = "../../../YelpData/SplitFiles/Split1/"
a = Naive_Bayes_Category_Classifier(training_path,testing_path,output_path)
