import re
import json

class BusinessObj(object):

    def __init__(self,id,numTerms,termFrequency):
        self.ID = id
        self.num = numTerms
        self.tf = termFrequency

    def getTF(word):
        if word in self.tf:
            return self.tf[word]
        else:
            return 0

class CategoryObj(object):

    def __init__(self,categoryName,numBusinesses,businessID):
        self.category = categoryName
        self.num = numBusinesses
        self.idDict = businessID
