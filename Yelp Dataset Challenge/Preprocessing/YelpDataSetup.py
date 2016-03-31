import re
import json
from Parser import *

BUSINESS_PATH = "../../../YelpData/yelp_academic_dataset_business.json"
REVIEW_PATH = "../../../YelpData/yelp_academic_dataset_review.json"

bdoc = open(BUSINESS_PATH)
rdoc = open(REVIEW_PATH)

#Parse business document with reviews
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
