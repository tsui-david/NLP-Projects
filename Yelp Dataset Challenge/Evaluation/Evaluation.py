import json

# precision
# categories predicted -> num_right/num_categories_predicted

# recall
# num predicted right out of categories predicted/num of correct categories

PATH_TO_ANSWERS = '../../../YelpTestData/testAnswers.json'
PATH_TO_PREDICTIONS = '../../../YelpTestData/prediction.json'

class Evaluation:

	def __init__(self):
		self.precision = {}
		self.precision['total_right'] = 0
		self.precision['total_guessed'] = 0

		self.recall = {}
		self.recall['total_right'] = 0
		self.recall['total_correct_answers'] = 0

		self.analyze()


	def analyze(self):
		with open(PATH_TO_ANSWERS) as a_file:					# testAnswers File

			with open(PATH_TO_PREDICTIONS) as p_file:			# predictions File
				for line in p_file:
					predicted_json = json.loads(line)
					predicted_answers = predicted_json["Predicted Categories"]
					ID = predicted_json["ID"]

					answers_json = json.loads(a_file.readline())
					correct_answers = answers_json['Categories']

					assert ID==predicted_json['ID']

					predicted_right = set(predicted_answers) & set(correct_answers)			# set of answers predicted right

					# calculate precision
					self.precision['total_right'] += len(predicted_right)
					self.precision['total_guessed'] += len(predicted_answers)

					# calculate recall
					self.recall['total_right'] += len(predicted_right)
					self.recall['total_correct_answers'] += len(correct_answers)


					print 'ID: %s' % (ID)
					print 'Predicted: %s' % (predicted_answers)
					print 'Correct: %s' % (correct_answers)
					print 'Guess Correct: %s' % (predicted_right)
					print ''

		precision = (float(self.precision['total_right'])/self.precision['total_guessed']) * 100
		recall = (float(self.recall['total_right'])/self.recall['total_correct_answers']) * 100
		print 'Precision: %s %%' % (precision)
		print 'Recall: %s %%' % (recall)


Evaluation()









