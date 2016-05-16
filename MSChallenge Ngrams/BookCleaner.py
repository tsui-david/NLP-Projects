from os import listdir
from os.path import isfile, join
from Tokenizer import *
import sys


class BookCleaner:
	onlyfiles=[]
	path = ''
	def __init__(self,mypath):
		#Get files in path directory
		self.onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		self.path = mypath
	def getCleanedTextSingleFile(self,file):
		row = file.readlines()
		for i in range(len(row)):
			if row[i].find("*END*THE SMALL PRINT! FOR PUBLIC DOMAIN") > -1:
				self.cleaned_str = row[i+1:]
				str = ''.join(self.cleaned_str)
				return str

	def getAllFilesCleaned(self):
		appendStr = ''
		for i, fileName in enumerate(self.onlyfiles):
			print "Current file %s, Current file index %d, Total %d" %(fileName,i,len(self.onlyfiles))
			str = '%s%s' %(self.path,fileName)
			file = open(str)
			str = (self.getCleanedTextSingleFile(file))
			appendStr = '%s%s' %(appendStr,str)
		return appendStr


path = ''
if len(sys.argv)==2:
	path = sys.argv[1]
else:
	print "No path input"
	sys.exit()

bc = BookCleaner(path)

reload(sys)
sys.setdefaultencoding('utf8')

#AGGREGATE RAW TEXT
text_file = open("big_training_raw.txt", "w+")
print "BookCleaner is now aggregating all texts"
str = bc.getAllFilesCleaned()
text_file.write(str)
text_file.close()
#TOKENIZE
print "Tokenizing texts"

text_file = open("tokenized_train.txt","w+")
file = open("big_training_raw.txt")
tk = Tokenizer()
for line in file:
		line = unicode(line, errors='replace')
		str=tk.tokenizeAdvanced(line)
		text_file.write(str)
text_file.close()