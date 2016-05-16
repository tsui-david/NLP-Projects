import json
import os

# precision
# categories predicted -> num_right/num_categories_predicted

# recall
# num predicted right out of categories predicted/num of correct categories

PATH_TO_ANSWERS = "../../../YelpDevData/naiveBayesTest.txt"
PATH_TO_PREDICTIONS = "../../../YelpDevData/prediction.txt"

PATH_TO_WEKA = '../../../YelpDevData/weka_test/'
PATH_TO_WEKA_PREDICTIONS = '../../../YelpDevData/wekapredictions.json'


# if prob of prediction of prediction is greater than this threshold than the category exists for the business
PREDICTION_THRESHOLD = 1


class Evaluation:

	# process_type: 1=bayes, 2=weka
	def __init__(self, process_type):
		self.precision = {}
		self.precision['total_right'] = 0
		self.precision['total_guessed'] = 0

		self.recall = {}
		self.recall['total_right'] = 0
		self.recall['total_correct_answers'] = 0

		# aggregrate valid predictions for every business
		if process_type==1:
			self.analyze(PATH_TO_PREDICTIONS)
		else:
			self.aggregate_predictions()
			self.analyze(PATH_TO_WEKA_PREDICTIONS)



	def aggregate_predictions(self):
		business_predictions = {}
		# must keep track of order in which business predictions are parsed to keep training and test data aligned
		order_business = []


		# fn == category name
		for fn in os.listdir(PATH_TO_WEKA):
			if fn == '.DS_Store':
				continue

			f = open(PATH_TO_WEKA + fn)

			# get category of current file
			curr_cat = f.readline().strip()
			for line in f:
				values = line.strip('\n').split()
				#print values

				b_id = values[1]

				prob = float(values[3])
				act_val = float(values[5])

				if b_id not in business_predictions:
					business_predictions[b_id] = {}
					business_predictions[b_id]['Predicted Categories'] = []
					order_business.append(b_id)


				if prob>=PREDICTION_THRESHOLD:
					business_predictions[b_id]['Predicted Categories'].append(curr_cat)

			f.close()




		with open(PATH_TO_WEKA_PREDICTIONS,'w+') as fn:
			for i in range(0, len(order_business)):
				ID = order_business[i]

				json_obj = {}
				json_obj["Predicted Categories"] = business_predictions[ID]['Predicted Categories']
				json_obj["ID"] = ID

				fn.write(json.dumps(json_obj) + '\n')




	def analyze(self, predictions_path):
		with open(PATH_TO_ANSWERS) as a_file:					# testAnswers File

			# {"Predicted Categories": ["Restaurants", "Traditional Chinese Medicine"], "ID": "if2t-pDVtB_TFUxAQW9Wzg"}
			with open(predictions_path) as p_file:			# predictions File
				for line in p_file:
					predicted_json = json.loads(line)
					predicted_answers = predicted_json["Predicted Categories"]
					ID = predicted_json["ID"]

					line = a_file.readline()

					try:
						answers_json = json.loads(line)
					except:
						print 'predictions file and test answers file has different num of business ids!'

					correct_answers = answers_json['Categories']

					assert ID==predicted_json['ID']

					predicted_right = set(predicted_answers) & set(correct_answers)			# set of answers predicted right

					# calculate precision
					self.precision['total_right'] += len(predicted_right)
					self.precision['total_guessed'] += len(predicted_answers)

					# calculate recall
					self.recall['total_right'] += len(predicted_right)
					self.recall['total_correct_answers'] += len(correct_answers)

					if len(predicted_right) > 0 :
						if not (len(list(predicted_right))==1 and list(predicted_right)[0]=='Restaurants'):
							print list(predicted_right)[0]
							# print 'ID: %s' % (ID)
							# print 'Predicted: %s' % (predicted_answers)
							# print 'Correct: %s' % (correct_answers)
							# print 'Guess Correct: %s' % (predicted_right)
							# print ''

		precision = (float(self.precision['total_right'])/self.precision['total_guessed']) * 100
		recall = (float(self.recall['total_right'])/self.recall['total_correct_answers']) * 100
		print 'Precision: %s %%' % (precision)
		print 'Recall: %s %%' % (recall)


Evaluation(1)
