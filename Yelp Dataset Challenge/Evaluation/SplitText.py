import os

# this class splits the data into five unique sets of test and training files to maximize variation

PERC_TRAINING_FILES = .80
PERC_TEST_FILES = (1-PERC_TRAINING_FILES)


PATH_TO_SPLIT_FOLDERS = '../../../YelpDevData/Split'

class SplitText:

	def __init__(self, path_to_json):
		self.reviews = list()

		if not os.path.exists(PATH_TO_SPLIT_FOLDERS+'1'):
			for i in range(1,6):
				os.makedirs(PATH_TO_SPLIT_FOLDERS+str(i))


		with open(path_to_json) as f:
			for line in f:
				self.reviews.append(line)

			self.num_of_reviews = len(self.reviews)
			self.interval_len = int(self.num_of_reviews*PERC_TEST_FILES)



			for i in range(1,6):		# we must create 5 sets of testing/training combos

				self.num_test = 0
				self.num_train = 0

				# range in 'reviews' in which we use as test files
				self.lower_bound = (i-1)*self.interval_len						# lower bound line num
				self.upper_bound = self.lower_bound + self.interval_len			# upper bound line num


				# gets paths that split training and test data will reside
				self.training_path = PATH_TO_SPLIT_FOLDERS + str(i) + '/training.txt'
				self.test_path = PATH_TO_SPLIT_FOLDERS + str(i) + '/test.txt'

				f_training = open(self.training_path, 'w+')
				f_test = open(self.test_path, 'w+')


				for n in range(0, self.num_of_reviews):						# iterate reviews
					if n in range(self.lower_bound, self.upper_bound):		# review is for test
						f_test.write(self.reviews[n])
						self.num_test += 1
					else:
						f_training.write(self.reviews[n])
						self.num_train += 1

				f_training.close()
				f_test.close()



path = '../../../YelpDevData/dev_business_cat.json'
SplitText(path)
