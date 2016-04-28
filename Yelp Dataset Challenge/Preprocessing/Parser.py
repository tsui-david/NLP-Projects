#Classses that will hold elements of business and categories
import re
import json


#Used to parse the raw json files
class BusinessParser(object):

    def __init__(self,id):
        self.id = id
        self.numReviews = 0
        self.numWords = 0
        self.review = []
        self.c = []
        self.dictionary = dict()
        self.attributes = {}
        self.raw_attributes = ""

    def addWords(self,text):
        words = re.split(" ",text)

        for word in words:
            if word in self.dictionary:
                self.dictionary[word] += 1
            else:
                self.dictionary[word] = 1
            self.numWords += 1
    def addText(self,text):
        self.review.append(text)
        self.numReviews += 1

        self.addWords(text)

    def addCategory(self,category):
        self.c = category

    def addAttribute(self,attribute, value):
        if attribute not in self.attributes:
            self.attributes[attribute] = value
    def addRawAttribute(self,raw_attribute):
        self.raw_attributes = raw_attribute

    def getAttributeVector(self,vector,cl):
        valueVector = [0]*(len(vector))

        for i in range(0,len(vector)):
            if(vector[i] in self.attributes):

                valueVector[i] = str(self.attributes[vector[i]])
            else:
                valueVector[i] = '?'
        if cl in self.c:
            valueVector.append(1)
        else:
            valueVector.append(0)

        s = ''
        for j in valueVector:
            s = s+str(j)+','
        s = s[:-1]
        return s

    #Pretty print json
    def toJSONPretty(self):
        return json.dumps({'ID':self.id,'Num Words':self.numWords,'Term Frequencies':self.dictionary, 'Categories':self.c, 'Attributes': self.raw_attributes},sort_keys=False, indent=4, separators=(',', ': '))
    #Json in one line for machine
    def toJSONMachine(self):
        print(self.c)
        return json.dumps({'ID':self.id,'Num Words':self.numWords,'Term Frequencies':self.dictionary, 'Categories':self.c, 'Attributes': self.raw_attributes},sort_keys=False)
class CategoryParser(object):

    def __init__(self,categoryName):
        self.name = categoryName
        self.bdict = []
        self.numBusinesses = 0
        self.aggregateReview = {}
        self.numWords = 0
    def addBusiness(self,id):
        self.bdict.append(id)
        self.numBusinesses += 1

    def updateReview(self,review,num):
        self.aggregateReview.update(review)
        self.numWords += num
    def toJSONPretty(self):
        return json.dumps({'Category':self.name,'Num Businesses':self.numBusinesses,'Business IDs':self.bdict, 'Term Frequencies':self.aggregateReview, 'Num Words':self.numWords},sort_keys=False, indent=4, separators=(',', ': '))

    def toJSONMachine(self):
        return json.dumps({'Category':self.name,'Num Businesses':self.numBusinesses,'Business IDs':self.bdict, 'Term Frequencies':self.aggregateReview, 'Num Words':self.numWords},sort_keys=False)

class WekaCategoryParser:
    def __init__ (self,key):
        self.name = key
        self.nominalValues = set()
    def addNominalValues(self,value):
        if value not in self.nominalValues:
            self.nominalValues.add(value)

    def getNominalValuesString(self):
        s = '{'
        for v in self.nominalValues:
            s += str(v)+','
        s = s[:-1]
        s += '}'
        return s

# b = BusinessParser(123)
# b.addText("HI this is david I am calling on behalf of sdlfjsdf")
# b.addText("Today is a great day. david are you there. I am calling you")
# b.addText("Today is an awesome day")
#
# c = CategoryParser("Cat")
# c.addBusiness(1)
# c.addBusiness(2)
# print(c.toJSON())
# print(b.toJSON())
