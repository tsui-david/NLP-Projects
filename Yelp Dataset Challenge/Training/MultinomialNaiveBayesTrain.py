import re
import json
from TrainParser import *

BUSINESS_PATH = "../../../YelpData/business.json"
CATEGORY_PATH = "../../../YelpData/category.json"
PREDICTION_OUTPUT_PATH = "../../../YelpData/prediction.json"

bdoc = open(BUSINESS_PATH)
cdoc = open(CATEGORY_PATH)
opdoc = open(PREDICTION_OUTPUT_PATH,"w+")

#Parse json files
bdict = {}
for line in bdoc:
    b = json.loads(line)
    print('working\n')
    bid = b['ID']
    bnum = b['Num Words']
    btf = b['Term Frequencies']

    if bid not in bdict:
        newBus = BusinessObj(bid,bnum,btf)
        bdict[bid] = newBus
    else:
        print "Error extra business id %s" % bid
        break

cdict = {}
for line in cdoc:
    c = json.loads(line)

    name = c['Category']
    cnum = c['Num Businesses']
    bids = c['Business IDs']

    if name not in cdict:
        newCat = CategoryObj(name,cnum,bids)
        cdict[name] = newCat
    else:
        print "Error extra category name %s" % name
        break
