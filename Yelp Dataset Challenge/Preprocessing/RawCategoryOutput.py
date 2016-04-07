import re
import json

BUSINESS_PATH = "../../../YelpData/small_business.json"
OUTPUT_PATH = "../../../YelpData/rawCategories.json"
bdoc = open(BUSINESS_PATH)
obdoc = open(OUTPUT_PATH, "w+")

cdict = {}
for line in bdoc:
    b = json.loads(line)
    categories = b['categories']
    for category in categories:
        if category not in cdict:
            cdict[category] = "nothing"

obdoc.seek(0,0)
obdoc.write(json.dumps({'Category Concepts':cdict},sort_keys=False, indent=4, separators=(',', ': ')))
