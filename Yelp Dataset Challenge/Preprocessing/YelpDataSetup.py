import re
import json
from Parser import *

BUSINESS_PATH = "../../../YelpData/small_business.json"
REVIEW_PATH = "../../../YelpData/small_review.json"
OUTPUT_BUSINESS_PATH = "../../../YelpData/business.json"
OUTPUT_CATEGORY_PATH = "../../../YelpData/category.json"

bdoc = open(BUSINESS_PATH)
rdoc = open(REVIEW_PATH)

obdoc = open(OUTPUT_BUSINESS_PATH, "w+")
ocdoc = open(OUTPUT_CATEGORY_PATH, "w+")
#Parse categories with businesses
cdict = {}
for line in bdoc:
    b = json.loads(line)
    bkey = b['business_id']
    categories = b['categories']

    for category in categories:
        if category not in cdict:
            Cat = CategoryParser(category)
            cdict[category] = Cat

        cdict[category].addBusiness(bkey)
#Parse business document with reviews
bdict = {}
for line in rdoc:
    b = json.loads(line)
    bkey = b['business_id']
    review = b['text']

    if bkey not in bdict:
        Bus = BusinessParser(bkey)
        bdict[bkey] = Bus

    bdict[bkey].addText(review)

#Write files

#Overwrite all previous file data
obdoc.seek(0,0)
for bkey in bdict:
    obdoc.write(bdict[bkey].toJSONMachine()+'\n')


ocdoc.seek(0,0)
for ckey in cdict:
    ocdoc.write(cdict[ckey].toJSONMachine()+'\n')
