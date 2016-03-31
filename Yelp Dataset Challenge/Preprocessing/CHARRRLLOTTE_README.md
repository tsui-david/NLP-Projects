#Integrating Preprocessing with Parse code
This will show you how to easily integrate the preprocessing with the current parse code

##Setup

The crux of the json parse code is found in YelpDataSetup.py, beginning in line 31
```
bdict = {}
for line in rdoc:
    b = json.loads(line)
    bkey = b['business_id']
    review = b['text']
```
##Implementation
This code will grab the business id and main text from the json file. Once you have that, you can proceed to text preprocess the text of the reviews.

##Output
You can output whatever you want. I'm currently thinking along the lines of a json file? Then I can just read it and output the term frequencies!
