#Preprocessing Yelp Data
This folder contains all the scripts that will be used to preprocess data.
The following files from Yelp Data Challenge will be used in this project:
  * yelp_academic_dataset_review.json
  * yelp_academic_dataset_business.json

Parser.py is a simple class file that makes up the data structure that will be used in other setup files.
Parser.py contains two helper classes: **BusinessParser** and **CategoryParser**.

BusinessParser holds a dictionary of texts of reviews and its frequency and the id of the business.
CategoryParser holds a set of business ids corresponding to the category.

##Setup
Run the YelpDataSetup.py to output a json file that will further be read from for training.
Make sure the change the filepath of the two Yelp Data files as needed!
**CURRENTLY IN PROGRESS**
