import re
import json
from Parser import *

BUSINESS_PATH = "../../../YelpData/yelp_academic_dataset_business.json"
REVIEW_PATH = "../../../YelpData/yelp_academic_dataset_review.json"
OUTPUT_BUSINESS_PATH = "./../../YelpData/business.json"
OUTPUT_CATEGORY_PATH = "./../../YelpData/category.json"

bdoc = open(BUSINESS_PATH)
rdoc = open(REVIEW_PATH)

obdoc = open(OUTPUT_BUSINESS_PATH, "rw+")
ocdoc = open(OUTPUT_CATEGORY_PATH, "rw+")
#Parse categories with businesses
cdict = {}
for line in bdoc:
    b = json.loads(line)
    bkey = b['business_id']
    categories = b['categories']

    for category in categories:
        if category in cdict:
            Cat = cdict[category]
        else:
            Cat = CategoryParser(category)
            cdict[category] = Cat

        Cat.addBusiness(bkey)
#Parse business document with reviews
bdict = {}
for line in rdoc:
    b = json.loads(line)
    bkey = b['business_id']
    review = b['text']

    if bkey in bdict:
        Bus = bdict[bkey]
    else:
        Bus = BusinessParser(bkey)
        bdict[bkey] = Bus

    Bus.addText(review)

#Write files

#Overwrite all previous file data
obdoc.seek(0,0)
for b in bdict:
    obdoc.write(b.toJSONMachine())

ocdoc.seek(0,0)
for c in cdict:
    ocdoc.write(c.toJSONMachine())
