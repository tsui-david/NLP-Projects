### TestTrainSetup is a simple python file that produces testing and training file in formatted json objects that both
### the naive bayes language model

## This is done AFTER the testing and training files have already been split from the raw files --> See background down below
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



class Naive_Bayes_Setup:

    def __init__(self,TRAIN_PATH,TEST_PATH,OUTPUT_PATH):
        ## -- PATHS --
        REVIEW_PATH = "../../../YelpData/processed_review.json"
        #Category is the training file for the multinomial naive bayes
        OUTPUT_CATEGORY_PATH = OUTPUT_PATH+"naiveBayesTrain.txt"
        #Test answer is the testing file for the logistic regression and naive bayes
        OUTPUT_TEST_PATH = OUTPUT_PATH+"naiveBayesTest.txt"

        ## -- GLOBAL VARIABLES --
        train_doc = open(TRAIN_PATH)
        test_doc = open(TEST_PATH)
        rdoc = open(REVIEW_PATH)
        ##Output files
        output_train_doc = open(OUTPUT_CATEGORY_PATH, "w+")
        output_test_doc = open(OUTPUT_TEST_PATH, "w+")
        ##Dictionary of reviews grouped by business ids


        ## -- BACKGROUND --
        # Testing and training files are split by business ids
        # Example: 80% 20% split will have 80% of the businesses be used for reviews and 20% of the businesses be used for testing
        # For naive bayes the reviews will be grouped by the business ids used for training will be grouped by categories

        print("Aggregating reviews by ids ...")
        ## -- NAIVE BAYES: AGGREGATE REVIEWS BY IDs --
        ## Group all reviews under each ID, this will be data that is shared by testing and training
        aggr_review_dict = {} #Dictionary of business class objects, keyed by business id
        for line in rdoc:
            b = json.loads(line)
            bkey = b['business_id']
            review = b['text']

            if bkey not in aggr_review_dict:
                Bus = BusinessParser(bkey)
                aggr_review_dict[bkey] = Bus
                aggr_review_dict[bkey].addText(review)
            else:
                aggr_review_dict[bkey].addText(review)

        print("Creating training files ...")
        ## -- NAIVE BAYES: Create training file
        cdict = {}  #Dictionary of category class objects, keyed by category name
        for line in train_doc:
            b = json.loads(line)
            bkey = b['business_id']
            categories = b['categories']
            attributes = b['attributes']
            if bkey in aggr_review_dict:
                bobj = aggr_review_dict[bkey]
                words = bobj.dictionary
                numWords = bobj.numWords
                for category in categories:
                    if category not in cdict:
                        Cat = CategoryParser(category)
                        cdict[category] = Cat

                    cdict[category].addBusiness(bkey)
                    cdict[category].updateReview(words,numWords)
        # Write to file
        for ckey in cdict:
            output_train_doc.write(cdict[ckey].toJSONMachine()+'\n')

        print("Creating test files ...")
        ## -- NAIVE BAYES: Create test file
        test_dict = {} #Dictionary of business class object, keyed by business ids
        for line in test_doc:
            b = json.loads(line)
            bkey = b['business_id']
            categories = b['categories']
            attributes = b['attributes']

            if bkey in aggr_review_dict:
                aggr_review_dict[bkey].addCategory(categories)
                aggr_review_dict[bkey].addRawAttribute(attributes)
                output_test_doc.write(aggr_review_dict[bkey].toJSONMachine()+'\n')

test_path = "../../../YelpData/SplitFiles/Split1/test.txt"
train_path = "../../../YelpData/SplitFiles/Split1/training.txt"
output_path = "../../../YelpData/SplitFiles/Split1/"
a = Naive_Bayes_Setup(train_path,test_path,output_path)
