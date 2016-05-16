import sys
import re

#--------------Functions----------------
def convertFraction(num,denom):	
	n = int(num)
	d = int(denom)
	if d == 0:
		return None
	elif d == 1:
		return convertNum(num)
	fract_bank = ['half','third','quarter']
	fract_bank2 = ['halves','thirds','quarters']
	
	num = convertNum(num)
	if d <= 4 and n > 1:
		denom = fract_bank2[d-2]
	elif d <= 4 and n == 1:
		denom = fract_bank[d-2]
	elif n > 1:
		denom = convertTH(denom)+"s"
	else:
		denom = convertTH(denom)

	return num+" "+denom

def convertYear(n):
	num = int(n)
	if(num >= 2000):
		print "working"
		a = convertNum(n)
		print "year",a
		return a
	else:
		chunk1 = convertNum(n[0:2])
		chunk2 = convertNum(n[2:4])
		return chunk1+" "+chunk2
def convertTH(n):
	if n == '0':
		return "zeroth"

	th_dict = ['zeroth','first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelfth','thirteenth','fourteenth','fifteenth',
	'sixteenth','seventeenth','eighteenth','nineteenth','twentieth']

	num = int(n)
	if(num<21):
		return th_dict[num]
	else:
		
		chunk = convertNum(n[:-1]+"0")
		last = th_dict[int(n[-1])]
		
		if last == "zeroth":
			print "worked"
			chunk = chunk[:-2]+"ieth"
			return chunk
		else:
			print "failed"
			return chunk+" "+last

def convertNumThrees(h,t,o):

	tens_plus = ['ten','twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
	single = ['zero','one','two','three','four','five','six','seven','eight','nine']
	tens = ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']

	one = int(o)
	ten = int(t)
	hundred = int(h)

	if h==0 and t == 0 and o == 0:
		return ""
	str = ""
	if one != 0:
		str = single[one]
	if ten == 1:
		str = tens[one]			#11,12,13,14,15 ... 19
	elif ten > 1 and one == 0:
		str = tens_plus[ten-1]	#20,30,40,50 ...... 90
	elif ten > 1:
		str = tens_plus[ten-1]+" "+str
	if hundred > 0 and (ten>0 or one>0):
		str = single[hundred]+" hundred "+str
	elif hundred > 0:
		str = single[hundred]+" hundred"

	return str
def convertNum(n):
	if n == "0":
		return "zero"
	hundreds = ['thousand','million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion', 'septillion']
	
	thirds = 0
	o = None
	t = None
	h = None

	if len(n) % 3 == 1:
		n= "00"+n
	elif len(n) % 3 == 2:
		n = "0"+n
	print n
	str=""
	#Start iterating from the first digit ie backwards
	for i in range(len(n)):
		digit = len(n) - i - 1
		
		if o is None:
			o = n[digit]
		elif t is None:
			t = n[digit]
		else:
			h = n[digit]
			chunk = convertNumThrees(h,t,o)

			if thirds > 0 and str != "" and chunk != "":
				print "here",str
				str = chunk+" "+hundreds[thirds-1]+" "+str
			elif thirds > 0 and chunk != "" and str == "":
				print "here1",str
				str = chunk+" "+hundreds[thirds-1]
			elif thirds > 0:
				chunk #Do nothing
			else:
				print "here2",str
				str = chunk

			thirds = thirds+1
			#Reset
			o = None
			t = None
			h = None
	return str


#--------------Translation function--------
def translate(input_str):
	#------------Ordinal numbers-------------
	#Accepts format of ordinal numbers - 1st,2nd,3rd,4th...
	ordinal_p = re.compile('([0-9]*[1])st|([0-9]*[2])nd|([0-9]*[3])rd|([0-9]*[0-9])th')

	p_parse = re.findall(ordinal_p,input_str)
	for parse in p_parse:
		print "---ordinal -----",parse
		if parse[0] !='':
			substitute = convertTH(parse[0])
		elif parse[1] != '':
			substitute = convertTH(parse[1])
		elif parse[2] != '':
			substitute = convertTH(parse[2])
		else:
			substitute = convertTH(parse[3])
		input_str = ordinal_p.sub(substitute,input_str,1)

	#------------Dollar----------------------
	#Accepts format of [$ x*.x* million]
	dollar_p2 = re.compile('\$ ([0-9]{1,3}(,[0-9]{3})+|[0-9]*)\.([0-9]+) (hundred|thousand|million|billion|trillion)',re.IGNORECASE)
	#Accepts format of [$ x million]
	dollar_p3 = re.compile('\$ ([0-9]{1,3}(,[0-9]{3})+|[0-9]+) (hundred|thousand|million|billion|trillion)',re.IGNORECASE)
	#Accepts format of [$ x*.xx]
	dollar_p0 = re.compile('\$ ([0-9]{1,3}(,[0-9]{3})+|[0-9]*)\.([0-9]+)')
	#Accepts format of [$ x]
	dollar_p1 = re.compile('\$ ([0-9]{1,3}(,[0-9]{3})+|[0-9]+)')

	p2_parse = re.findall(dollar_p2,input_str)
	for parse in p2_parse:
		print "--dollar 2--",parse
		parsed = parse[0].replace(",","")
		print "removed comma: ",parsed
		substitute = convertNum(parsed)+" point "+convertNum(parse[2])+" "+parse[3]+" dollars"
		input_str = dollar_p2.sub(substitute,input_str,1)

	p3_parse = re.findall(dollar_p3,input_str)
	for parse in p3_parse:
		print "--dollar 3--",parse
		parsed = parse[0].replace(",","")
		print "removed comma: ",parsed
		substitute = convertNum(parsed)+" "+parse[2]+" dollars"
		input_str = dollar_p3.sub(substitute,input_str,1)

	p0_parse = re.findall(dollar_p0,input_str)
	for parse in p0_parse:
		print "--dollar 0--",parse
		parsed = parse[0].replace(",","")
		print "removed comma: ",parsed
		if parsed is not '' and int(parsed) > 0:
			d = convertNum(parsed)
			s1 = " dollars and "
			if int(parsed) == 1:
				s1 = " dollar and "

			if len(parse) == 3:
				parse_cent = parse[2] #Dealing with commas		
			else:
				parse_cent = parse[1]
			if len(parse_cent) == 2:
				substitute = convertNum(parsed)+s1+convertNum(parse_cent)+" cents"
			elif len(parse_cent) == 1:
				substitute = convertNum(parsed)+s1+convertNum(parse_cent+"0")+" cents"
			else:
				substitute = convertNum(parsed)+s1+convertNum(parse_cent[:2])+" point "+convertNum(parse_cent[2:])+" cents"
		else:
			parse_cent = parse[1]
			if len(parse_cent) == 2:
				substitute = convertNum(parse_cent)+" cents"
			elif len(parse_cent) == 1:
				substitute = convertNum(parse_cent+"0")+" cents"
			elif len(parse_cent) == 3:
				substitute = convertNum(parse_cent[:2])+" point "+convertNum(parse_cent[2:])+" cents"
		input_str = dollar_p0.sub(substitute,input_str,1)

	p1_parse = re.findall(dollar_p1,input_str)
	for parse in p1_parse:

		print "--dollar 1--",parse
		parsed = parse[0].replace(",","")
		print "removed comma: ",parsed
		d = convertNum(parsed)
		s1 = " dollars"
		if int(parsed) == 1:
			s1 = " dollar"
		substitute = convertNum(parsed)+s1
		input_str = dollar_p1.sub(substitute,input_str,1)
	#------------Fraction--------------------
	#Accepts format of [x x\/x]
	fraction_p0 = re.compile('([0-9]+) ([0-9]+)\\\/([0-9]+)')
	#Accepts format of [x\/x]
	fraction_p1 = re.compile('([0-9]+)\\\/([0-9]+)')

	p0_parse = re.findall(fraction_p0,input_str)
	for parse in p0_parse:
		print "--fraction 0 --"
		num = parse[1]
		denom = parse[2]
		substitute = parse[0]+" and "+convertFraction(num,denom)
		input_str = fraction_p0.sub(substitute,input_str,1)

	p1_parse = re.findall(fraction_p1,input_str)
	for parse in p1_parse:
		print "--fraction 1--"
		num = parse[0]
		denom = parse[1]
		substitute = convertFraction(num,denom)
		input_str = fraction_p1.sub(substitute,input_str,1)

	#------------Percents--------------------
	#Accepts format of [x*.x+ %]
	percent_p0 = re.compile('([0-9]*)\.([0-9]+) %')
	#Accepts format of [x %]
	percent_p1 = re.compile('([0-9]+) %')
	percent_p2 = re.compile('%')

	p0_parse = re.findall(percent_p0,input_str)
	for parse in p0_parse:
		print "--percent 0--"
		if parse[0] is not '':
			substitute = convertNum(parse[0])+" point "+convertNum(parse[1])+" percent"
		else:
			substitute = "point "+convertNum(parse[1])+" percent"
		input_str = percent_p0.sub(substitute,input_str,1)

	p1_parse = re.findall(percent_p1,input_str)
	for parse in p1_parse:
		print "--percent 1--"
		substitute = convertNum(parse)+" percent"
		input_str = percent_p1.sub(substitute,input_str,1)
	
	p2_parse = re.findall(percent_p2,input_str)
	for parse in p2_parse:
		print "--percent 1--"
		substitute = "percent"
		input_str = percent_p2.sub(substitute,input_str,1)
	#------------Dates-----------------------
	#Accepts format of [month day , year]
	dates_p0 = re.compile('(january|jan\.?|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sept\.?|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december) ([0-9]{1,2}) , ([0-9]{4})', re.IGNORECASE)
	#Accepts format of [month year]
	dates_p1 = re.compile('(january|jan\.?|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sept\.?|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december) ([0-9]{4})', re.IGNORECASE)
	#Accepts format of [month day]
	dates_p2 = re.compile('(january|jan\.?|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sept\.?|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december) ([0-9]{1,2})',re.IGNORECASE)
	#Accepts format of [until year|in year]
	dates_p3 = re.compile('(until|in) ([0-9]{4})',re.IGNORECASE)

	p0_parse = re.findall(dates_p0,input_str)
	for parse in p0_parse:
		print "--date 0---",parse
		substitute = "\\1 "+convertTH(parse[1])+" , "+convertYear(parse[2])
		input_str = dates_p0.sub(substitute,input_str,1)

	p1_parse = re.findall(dates_p1,input_str)
	for parse in p1_parse:
		print "---date 1---",parse
		substitute = "\\1 "+convertYear(parse[1])
		input_str = dates_p1.sub(substitute,input_str,1)

	p2_parse = re.findall(dates_p2,input_str)
	for parse in p2_parse:
		print "--date 2--", parse
		substitute = "\\1 "+convertTH(parse[1])
		input_str = dates_p2.sub(substitute,input_str,1)

	p3_parse = re.findall(dates_p3,input_str)
	for parse in p3_parse:
		print "--date 3--", parse
		substitute = parse[0]+" "+convertYear(parse[1])
		input_str = dates_p3.sub(substitute,input_str,1)
	#-----------Normal-------------------------
	#Accepts format .x for number
	normal_p = re.compile('([0-9]{1,3}(,[0-9]{3})+|[0-9]*)\.([0-9]+)')
	#Accepts format x,xxx for number
	normal_p0 = re.compile('([0-9]{1,3}(,[0-9]{3})+)')
	#Accepts any number
	normal_p1 = re.compile('[0-9]+')

	p_parse = re.findall(normal_p,input_str)
	for parse in p_parse:
		print "--norm decimal--",parse

		if parse[0]=='':
			substitute = " point "+convertNum(parse[2])
			input_str = normal_p.sub(substitute,input_str,1)
		else:
			parsed = parse[0].replace(",","")
			print "removed comma: ",parsed
			substitute = convertNum(parsed)+" point "+convertNum(parse[2])
			input_str = normal_p.sub(substitute,input_str,1)
	p0_parse = re.findall(normal_p0,input_str)
	for parse in p0_parse:
		print "--norm 0--",parse
		parsed = parse[0].replace(",","")
		print "removed comma: ",parsed
		input_str = normal_p0.sub(convertNum(parsed),input_str,1)

	p1_parse = re.findall(normal_p1,input_str)
	for parse in p1_parse:
		print "--norm 1--",parse
		substitute = convertNum(parse)
		print substitute
		input_str = normal_p1.sub(substitute,input_str,1)

	

	

	print "FINAL: --"
	print input_str
	return input_str

#----Main---------------------
if len(sys.argv) < 3:
	print("ERROR----Not enough arguments-----ERROR")
	sys.exit(0)
# Open a file
fi = open(sys.argv[1],"r")
fo = open(sys.argv[2], "wb+")
#
#print(translate("1,234.567"))
fo.write(translate(fi.read()))

# Close opend file
fo.close()
fi.close()


