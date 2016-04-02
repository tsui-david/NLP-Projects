import re
import json
from TrainParser import *

#BUSINESS_PATH = "../../../YelpData/business.json"
CATEGORY_PATH = "../../../YelpData/category.json"
PREDICTION_OUTPUT_PATH = "../../../YelpData/prediction.json"

#bdoc = open(BUSINESS_PATH)
cdoc = open(CATEGORY_PATH)
opdoc = open(PREDICTION_OUTPUT_PATH,"w+")

#Parse json files
cdict = {}
for line in cdoc:
    c = json.loads(line)
    cName = c['Category']
    cTF = c['Term Frequencies']
    cNum = c['Num Words']
    if cName not in cdict:
        newCat = CategoryObj(cName,cNum,cTF)
        cdict[cName] = newCat
    else:
        print "Error extra business id %s" % bid
        break
