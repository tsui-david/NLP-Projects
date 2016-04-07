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


## Charlotte's Preprocessing Note

Stemming/Lemmatization Process:
- Use nltk "wordpunct_tokenize" to tokenize each line by white space and punctuation
- Remove recurring punctuations
- Decapitalize each word in each line
- Remove all pronouns 
- Remove all apostrophes (e.g. "'s", "'ve")

- Use nltk "PorterStemmer" to stem each word in the line
- Remove all extra spaces in the final preprocessed sentence