###Raw preprocess is a simple python file that reduces the categories available in Yelp to the root categories
### and preprocesses all the text by lemmatization
###Uses the raw json files of Yelp: business.json and review.json

###Review.json is used for the naive bayes training and testing
###Business.json stores all the information on the businesses, it is used for both logistic regression and naive bayes
import re
import json
import ast
import nltk
from Parser import *
from Preprocess import *
from nltk.stem.porter import PorterStemmer
from nltk.metrics import edit_distance
from nltk.tokenize import wordpunct_tokenize
from xlrd import open_workbook

## -- PATHS --
BUSINESS_PATH = "../../../YelpDevData/dev_cact.json"
REVIEW_PATH = "../../../YelpData/yelp_academic_dataset_review.json"
OUTPUT_BUSINESS_PATH = "../../../YelpData/processed_business_big.json"
OUTPUT_REVIEW_PATH = "../../../YelpData/processed_review_big.json"
#Train answer is the training file for the logistic regression
OUTPUT_TRAIN_PATH = "../../../YelpData/trainAnswers_big.json"
#Category is the training file for the multinomial naive bayes
OUTPUT_CATEGORY_PATH = "../../../YelpData/category_big.json"
#Test answer is the testing file for the logistic regression and naive bayes
OUTPUT_TEST_PATH = "../../../YelpData/testAnswers_big.json"
CATEGORY_YELP_HIERARCHY_PATH = "../../../YelpData/yelp-business-categories-list.xlsx"

## -- GLOBAL VARIABLES --
bdoc = open(BUSINESS_PATH)
rdoc = open(REVIEW_PATH)
excel_doc = open_workbook(CATEGORY_YELP_HIERARCHY_PATH).sheet_by_index(0)
##Output files
output_preprocessed_business = open(OUTPUT_BUSINESS_PATH,"w+")
output_preprocessed_review = open(OUTPUT_REVIEW_PATH,"w+")

obdoc = open(OUTPUT_TEST_PATH, "w+")
ocdoc = open(OUTPUT_CATEGORY_PATH, "w+")

#Store business document with reviews from the review.json
trainDict = {}  #Training business dictionary
testDict = {} #Testing business dicitonary
#Store the list of simplified categories from all the sub categories of yelp
main_category_list = []

## --- PARENT CATEGORY EXCEL FILE EXTRACTION --
## Stores all the main categories to main_category_list from the yelp hierarchy excel file
cat_count = 0;
for rownum in range(3, excel_doc.nrows):
    cat = str(excel_doc.cell(rownum, 0).value)
    if cat != '':
        main_category_list.append(cat)
        cat_count += 1

## -- CATEGORY FILTER --
## Goes through business.json and filter through all categories not belonging in the main categories
for line in bdoc:
    entry = line.strip('\n')
    json_obj = json.loads(entry)
    for cat in list(json_obj['categories']):
        index = json_obj['categories'].index(str(cat))
        if json_obj['categories'][index] not in main_category_list:
            del json_obj['categories'][index]
    entry = json.dumps(json_obj)
    output_preprocessed_business.write(str(entry)+"\n")
#
# ## -- WORD STEMMING --
# ## Goes through review.json and lemmatize all review words
# porter_stemmer = PorterStemmer()
# for line in rdoc:
#     b = json.loads(line)
#     bkey = b['business_id']
#     review = b['text']
#
#     # tokenize the sentence by white space and punctuations; prepare for stemming
#     new_sent = wordpunct_tokenize(review)
#
#     new_review = ''
#     # stem each words in the sentence
#     for w in new_sent:
#         # remove recurring punctuations and special punctuations
#         w = removeExtraPunc(w)
#         # decapitalize each word
#         w = w.lower()
#         # remove pronouns
#         w = removePronouns(w, True)
#         # remove preposition
#         w = removePrepositions(w)
#
#         w = removeBe(w)
#         w = removeConjunction(w)
#
#         w = removeNumbers(w)
#
#         # remove apostrophe & postfix of Apostrophe
#         w = removeApostrophe(w, True)
#         w = removePostfixApos(w, True)
#
#         # Stemming
#         new_review += porter_stemmer.stem(w)
#         new_review += " "
#
#     # remove extra spaces
#     new_review = removeMultipleSpaces(new_review)
#     b['text'] = new_review
#     entry = json.dumps(b)
#     output_preprocessed_review.write(str(entry)+"\n")

## -- END --
bdoc.close()
rdoc.close()
output_preprocessed_review.close()
output_preprocessed_business.close()
