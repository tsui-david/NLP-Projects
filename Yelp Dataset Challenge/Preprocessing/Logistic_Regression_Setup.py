import re
import json
from Parser import *

#TEST_PATH = "../DataOutput/test.txt"
#INPUT_PATH = "../../../YelpData/small_business.json"
BUSINESS_PATH = "../../../YelpData/testAnswers.json"


bdoc = open(BUSINESS_PATH)


categoriesSet = set()
catA = []

attDict = {}

tbusiness = []

for line in bdoc:
    b = json.loads(line)
    bkey = b['ID']
    categories = b['Categories']

    bus = BusinessParser(bkey)

    for cat in categories:
        if cat not in categoriesSet:
            categoriesSet.add(cat)
            catA.append(cat)

    bus.addCategory(categories)
    attributes = b['Attributes']

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
size = len(catA)
for i in catA:


    key = i
    i = i.replace("/","")
    i = i.replace(" ","")
    print str(count)+' of '+str(size)
    print i
    count+=1
    OUTPUT_WEKA_PATH = "../../../YelpData/weka/"+i+".arff"
    #OUTPUT_WEKA_PATH = "../DataOutput/"+i+".arff"

    owdoc = open(OUTPUT_WEKA_PATH, "w+",0)
    owdoc.seek(0,0)
    owdoc.write('%Category: '+key+'\n')
    owdoc.write('@Relation '+i+'\n\n')


    for a in attDict:

        owdoc.write('@ATTRIBUTE '+str(a)+' '+attDict[a].getNominalValuesString()+'\n')

    #Get string of array
    owdoc.write('@ATTRIBUTE class {0,1}\n')
    owdoc.write('@DATA\n')

    count2 = 0
    for b in tbusiness:
        count2 += 1
        owdoc.write(b.getAttributeVector(attA,key)+'\n')
    print(count2)
    owdoc.close()
