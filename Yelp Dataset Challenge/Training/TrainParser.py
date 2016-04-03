import re
import json

class BusinessObj(object):

    def __init__(self,id,category):
        self.ID = id
        self.Category = category
    def toJSONMachine(self):
        return json.dumps({'ID':self.ID,'Predicted Categories':self.Category},sort_keys=False)

class CategoryObj(object):

    def __init__(self,categoryName,numWords,termFrequency):
        self.category = categoryName
        self.numWords = numWords
        self.termFrequency = termFrequency
        self.wordSetSize = len(self.termFrequency)

    def getTF(self,word):
        if word in self.termFrequency:
            return self.termFrequency[word]
        else:
            return 0
