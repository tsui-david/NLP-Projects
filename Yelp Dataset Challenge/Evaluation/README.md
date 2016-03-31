#Evaluation of YELP Dataset
This folder will contain all scripts pertaining to the evaluation of the business classifier

##Input
The business classifier will have outputted in JSON format a text of business ids and predicted categories.
An example of the input can be something like this:

```
{
  "Business ID": x123lkj,
  "Predicted Categories": ["Coffee","Cats","Shibas","Awesome"]
}
```

This will be all on a single line. Each line will be a separate json file.

##Implementation
We should try to match the predicted and correct categories and see evaluate how many we get right. This is text book precision and recall problem since we might have missing categories that we did not predict and categories that we predicted wrong.

##Output
Up to you! But we should at least have an overall accuracy.
