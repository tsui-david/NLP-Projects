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
        self.categories = []
        self.dictionary = dict()

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

    #Pretty print json
    def toJSONPretty(self):
        return json.dumps({'ID':self.id,'Num Words':self.numWords,'Term Frequencies':self.dictionary},sort_keys=False, indent=4, separators=(',', ': '))
    #Json in one line for machine
    def toJSONMachine(self):
        return json.dumps({'ID':self.id,'Num Words':self.numWords,'Term Frequencies':self.dictionary},sort_keys=False)
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
