--------------------------------------------------------------
David Tsui
Human Languages and Technologies
Spring 2016
Dr. Rebecca Hwa

Assignment 2 Readme
--------------------------------------------------------------
--------------------------------------------------------------
Part 2 Run Program Instructions
--------------------------------------------------------------
To run the program for part 2 of the assignment,
run the command in terminal with the following format:

Ngram.py <1|2|2s|3|3s> <trainfile> <devfile> <testfile>

Where <1|2|2s|3|3s> represents the type of models,
trainfile is the name of the train file, devfile is the
name of the devfile, and testfile is the name of the test file.


The file outputs a text file called part2_output.txt containing the 
*Note* Ngrams.py is the file for Ngram classes while Ngram.py
simply handles assignment 2 part 2's problem

--------------------------------------------------------------
Part 3 Run Program Instructions and Details
--------------------------------------------------------------
The part 3 assignment is broken down into several components for
the sake of easier debugging and modularity.

The pipeline follows with:
	1. Aggregate all training file text into one raw text file

		This is done by going to the directory of where all the training
		files are located and reading each file and writing to one single
		file

		BookCleaner.py is a class that does this upon the initialization.

	2. Clean Project Guttenberg texts

		Every Project Guttenberg text has meta data and an introduction
		to Project Guttenberg that is not actually in the book itself.

		To get rid of the header, BookCleaner.py appends only content of the
		text file after the line which contains "*END*THE SMALL PRINT! FOR PUBLIC DOMAIN"

	3. Tokenize Project Guttenberg texts by labelling sentence boundaries
	with <s> and </s>

		I used a tokenizing library called NLTK and the PUNKT package that
		uses the data library "english.pickle" to segment each sentence.

	4. Cleaning tokenized texts by removing punctuations and lowercasing
	all texts

		To ensure that all texts are consistent, I removed all punctuations and
		lowercased the texts. This allows for words within quotations to be equal
		to words without quotation. Same goes for capitalized vs non-capitalized
		words.

	To accomplish steps 1-4:
	run the command in the terminal with the following format:

		>>python BookCleaner.py <path>

		Where path is the path to the file directory such as:
		/Users/david/Downloads/Holmes_Training_Data/

		The command will output the training files:
		*big_train.txt*, which is the aggregate of all the files under Holmes_Training_Data
		*tokenized_train.txt*, which is the tokenized version of big_train.txt

	5. Train vocabulary with trigram smoothed

		I used trigram smoothed model because during development testing I found that 
		trigram model gave the most accuracy.

		The settings are:
			Unigram lambda = .3
			Bigram lambda = .3
			Trigram lambda = .4

	6. Read development and test file and output perplexity for each line

		MSChallengeNGrams.py will read in the file Holmes.lm_format.questions.txt which will have all
		the sentences as choices in groups of 5. It will then go through and calculate the 
		perplexity for each sentence and output it as "holmes_output.txt.txt"

	To accomplish steps 5-6,
	run the command in the terminal with the following format:

		>>python MSChallengeNGrams.py

	7. Compare for accuracy

	To accomplish step 7:
	run the command in the terminal with teh following format:

		>>cat holmes_output.txt.txt | ./bestof5.pl > tmp.txt ./score.pl tmp.txt Holmes.lm_format.answers.txt

--------------------------------------------------------------------------------------------------
 Write UP  Question 1:
 	What problems can occur (or  have occurred  in your experiments, if there is any) when
	the N ­ gram language model you implemented in Part I is trained on a  large training data such
	as the Project Gutenberg? Given that you have access to the development data, how did it help
	you to adapt and/or train your models?
--------------------------------------------------------------------------------------------------

	Most of the problem came from the getting the formatting of the input to work correctly. In part 1
	and 2 the format of the language input was very simple with period and commas as quotations. In
	the Guttenberg texts there are many punctuations and different white spacing that can mess with
	how the program runs. Thus, a lot of preprocessing had to be done in order for the N gram language
	model from part 1 and 2 to work.

	In addition, the script for score comparison looks for the bigger value as the better score in
	a sentence. As a result, the N gram model returns the perplexity multiplied by -1.

	The development data helps me to tweak the lambda values for the trigram smoothing model.
	By adjusting and tweaking the lambda values to get the optimal accuracy, the model is better
	adapted to the lm_question.txt

--------------------------------------------------------------------------------------------------
 Write UP  Question 2:
 	How did your models perform? Were they as you expected? Why wasn’t the  N­ gram language
 	model alone good enough for the sentence completion task? What additional
 	tools or techniques do you think are necessary? Can the language model itself be
 	changed to account for more ambiguities?
--------------------------------------------------------------------------------------------------

	The results of the language model is:
	389 of 1040 correct
	Overall average: 37.4038461538462%
	dev: 38.8461538461538%
	test: 35.9615384615385%

	The model performed better than random guessing since a random guess would be 20% accuracy.
	This result is within expectation because the model is trained on a large text data and
	thus can model the language better than randomly guessing. It does attain a high accuracy
	because the questions are in part designed to be hard against Ngrams. This is because the
	Ngram models do not have any context recognition or part of speech tagging that gives meaning
	to the words within the sentence. Instead the language model uses frequencies of words.

	By incorporating parts of speech tagging, there can be some increase in context recognition
	within the questions and answers.

	The language model can be improved with increase to the Ngram as increasing Ngram will more
	closely model the language. As well, discounting the words through Good-Turing method or other
	discount methods will help to smooth out the 0 frequencies of words for the trigram, bigram models.

	In this way the trigram model or bigram model will not be abandoned during interpolation
	when the phrases do not match.