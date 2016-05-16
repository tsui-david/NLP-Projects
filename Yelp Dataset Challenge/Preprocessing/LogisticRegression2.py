## Logistic regression setup produces testing and training file for the logistic regression classifier in weka
## Outputs .arff files that is used in weka
import re
import json
import os
from Parser import *

class logistic_setup:


    def __init__(self,INPUT_PATH,OUTPUT_PATH):
        doc = open(INPUT_PATH)
        writer = open(OUTPUT_PATH, "w+")

        categoriesSet = set()
        trainCat = []
        attDict = {}
        tbusiness = []
        for line in doc:
            b = json.loads(line)
            bkey = b['business_id']
            categories = b['categories']

            bus = BusinessParser(bkey)

            for i in range(0,len(categories)):
                s = categories[i].strip()
                s = s.replace(" ","")
                s = s.replace("&","")
                categories[i] = s

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
            tbusiness.append(bus)


        attA = []
        for a in attDict:
            attA.append(a)
        #Create arff file
        count = 0
        size = len(trainCat)

        writer.write('@Relation LogisticRegression \n')
        for a in attDict:
            writer.write('@ATTRIBUTE '+str(a)+' '+attDict[a].getNominalValuesString()+'\n')

        class_str = ""
        for cat in categoriesSet:
            class_str+=str(cat)+","
        class_str = class_str[:-1]

        #Get string of array
        writer.write('@ATTRIBUTE class {'+class_str+'}\n')
        writer.write('@DATA\n')

        count2 = 0
        for b in tbusiness:
            if(len(b.c)==1):
                writer.write(b.getAttributeVectorTest(attA)+'\n')
        print(count2)
        writer.close()



INPUT_PATH = "../../../YelpData/processed_business.json"
OUTPUT_PATH = "../../../YelpData/wekaLogisticOutput.arff"
a = logistic_setup(INPUT_PATH,OUTPUT_PATH)
