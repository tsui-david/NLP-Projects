## Logistic regression setup produces testing and training file for the logistic regression classifier in weka
## Outputs .arff files that is used in weka
import re
import json
import os
from Parser import *

class logistic_setup:
    def __init__(self,TRAIN_PATH,TEST_PATH,OUTPUT_PATH):
        train_doc = open(TRAIN_PATH)
        test_doc = open(TEST_PATH)

        if not os.path.exists(OUTPUT_PATH+"weka_train"):
				os.makedirs(OUTPUT_PATH+"weka_train")
        # if not os.path.exists(OUTPUT_PATH+"weka_test"):
        #         os.makedirs(OUTPUT_PATH+"weka_test")

        ## -- SETUP TRAIN CATEGORY OBJECTS --
        categoriesSet = set()
        trainCat = []
        attDict = {}
        train_business = []
        for line in train_doc:
            b = json.loads(line)
            bkey = b['business_id']
            categories = b['categories']

            bus = BusinessParser(bkey)

            for cat in categories:
                if cat not in categoriesSet:
                    categoriesSet.add(cat)
                    trainCat.append(cat)

            bus.addCategory(categories)
            attributes = b['attributes']

            for i in attributes:
                if isinstance(attributes[i],dict):
                    for j in attributes[i]:
                        key = j
                        j = j.replace(" ","")

                        if j not in attDict:
                            attDict[j] = WekaCategoryParser(j)
                        bus.addAttribute(j,attributes[i][key])
                        attDict[j].addNominalValues(attributes[i][key])
                else:
                    key = i
                    i = i.replace(" ","")
                    if i not in attDict:
                        attDict[i] = WekaCategoryParser(i)
                    bus.addAttribute(i,attributes[key])
                    attDict[i].addNominalValues(attributes[key])
            train_business.append(bus)



        test_business = []
        ## -- SETUP TEST CATEGORY OBJECTS --

        for line in test_doc:
            b = json.loads(line)
            bkey = b['business_id']
            categories = b['categories']

            bus = BusinessParser(bkey)

            for cat in categories:
                if cat not in categoriesSet:
                    categoriesSet.add(cat)
                    trainCat.append(cat)

            bus.addCategory(categories)
            attributes = b['attributes']

            for i in attributes:
                if isinstance(attributes[i],dict):
                    for j in attributes[i]:
                        key = j
                        j = j.replace(" ","")

                        if j not in attDict:
                            attDict[j] = WekaCategoryParser(j)
                        bus.addAttribute(j,attributes[i][key])
                        attDict[j].addNominalValues(attributes[i][key])
                else:
                    key = i
                    i = i.replace(" ","")
                    if i not in attDict:
                        attDict[i] = WekaCategoryParser(i)
                    bus.addAttribute(i,attributes[key])
                    attDict[i].addNominalValues(attributes[key])
            test_business.append(bus)


        ## -- Write out training file --
        attA = []
        for a in attDict:
            attA.append(a)
        #Create arff file
        count = 0
        size = len(trainCat)





        attA = []
        for a in attDict:
            attA.append(a)
        #Create arff file
        count = 0
        size = len(trainCat)
        for i in trainCat:
            key = i
            i = i.replace("/","")
            i = i.replace(" ","")
            print str(count)+' of '+str(size)
            print i
            count+=1
            OUTPUT_WEKA_PATH = str(OUTPUT_PATH+"weka_train/"+i+".arff")
            #OUTPUT_WEKA_PATH = "../DataOutput/"+i+".arff"
            print("PATH: "+OUTPUT_WEKA_PATH)
            owdoc = open(OUTPUT_WEKA_PATH, "w+")
            owdoc.seek(0,0)
            owdoc.write('%Category: '+key+'\n')
            owdoc.write('@Relation '+i+'\n\n')


            for a in attDict:
                owdoc.write('@ATTRIBUTE '+str(a)+' '+attDict[a].getNominalValuesString()+'\n')

            #Get string of array
            owdoc.write('@ATTRIBUTE class {0,1}\n')
            owdoc.write('@DATA\n')

            count2 = 0
            for b in train_business:
                count2 += 1
                owdoc.write(b.getAttributeVector(attA,key)+'\n')
            print(count2)
            owdoc.close()


        ## -- Write test file --
        OUTPUT_WEKA_PATH = str(OUTPUT_PATH+"weka_test.arff")
        OUTPUT_WEKA_ANSWER_PATH = str(OUTPUT_PATH+"weka_testAnswers.txt")

        owdoc = open(OUTPUT_WEKA_PATH, "w+")
        testAnswers = open(OUTPUT_WEKA_ANSWER_PATH, "w+")

        owdoc.write('@Relation Logistic\n')
        for a in attDict:
            owdoc.write('@ATTRIBUTE '+str(a)+' '+attDict[a].getNominalValuesString()+'\n')

        #Get string of array
        owdoc.write('@ATTRIBUTE class {0,1}\n')
        owdoc.write('@DATA\n')

        count2 = 0
        for b in test_business:
            count2+=1
            owdoc.write(b.getAttributeVector(attA,'?')+'\n')

            json_obj = {}
            json_obj["Categories"] = b.c
            json_obj["ID"] = str(count2)

            testAnswers.write(json.dumps(json_obj) + '\n')

        print(count2)


test_path = "../../../YelpDevData/test.txt"
train_path = "../../../YelpDevData/training.txt"
output_path = "../../../YelpDevData/"
a = logistic_setup(train_path,test_path,output_path)
