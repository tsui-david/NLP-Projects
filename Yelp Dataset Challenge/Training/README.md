#Training for Yelp Dataset
This is the folder which holds all the scripts for training the dataset of the yelp dataset challenge

##Input
The training file will be the preprocessed output from the preprocessing script: **YelpDataSetup.py**. The default preprocessed output from the YelpDataSetup.py is:

  * **business.json**
      ```
      Example:
      {
        "ID":123,
        "Num Words":2430,
        "Term Frequencies":
            {
              "service":123,
              "to":240,
              ...
            }
      }
      ```
  * **category.json**
      ```
      Example:
      {
        "Category":"Grocery",
        "Num Businesses":40,
        "Business IDs":
            {
              "123",
              "456",
              ...
            }
      }
      ```
##Implementation
The basic training implementation will be using the bag of words and naive bayes approach to create a maximum likelihood estimation of the category given a review.

The algorithm used is the multinomial model that can be referred in the final report in the folder above.
