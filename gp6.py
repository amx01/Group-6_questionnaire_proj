# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Import basic Python libraries for use in your program: [os.path](http://docs.python.org/2/library/os.path.html) and [ConfigParser](http://docs.python.org/2/library/configparser.html)

# <codecell>

import os.path
import ConfigParser

# <markdowncell>

# An example of reading data from a Google Spreadsheet using the gspread library: http://stackoverflow.com/a/18296318/462302
# 
# First you'll need to install the gspread library on your virtual machine using: `sudo pip install gspread`

# <codecell>

import gspread

# <markdowncell>

# Define `take(n, iterable)` which is a convenience function to limit the amount of output that you print. Useful when you have lots of data that will clutter up your screen!

# <codecell>

from itertools import islice
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

# <markdowncell>

# Read the username and password from the `[google]` section of the `stat157.cfg` config file from your virtual machine home directory.

# <codecell>

home = os.path.expanduser("~")
configfile = os.path.join(home, 'stat157.cfg')
config = ConfigParser.SafeConfigParser()
config.read(configfile)
username = config.get('google', 'username')
password = config.get('google', 'password')
print username

# <markdowncell>

# Read the docid of the Google Spreadsheet from the config file.

# <codecell>

docid = config.get('questionnaire', 'docid')
client = gspread.login(username, password)
spreadsheet = client.open_by_key(docid)
worksheet = spreadsheet.get_worksheet(0)
print docid

# <markdowncell>

# Add field names to this list to include the column from the Google Spreadsheet in the filtered data output. You should choose one other column in addition to the learning style column. Refer to README.md from the homework assignment.

# <codecell>

#fieldnames = ['Timestamp','What is your learning style?']
col1Key = 'What is your learning style?'
col2Key = u'How often do you take the following roles in group projects? [A producer. This person knows how to get the job done.\xa0]'
fieldnames = [col1Key, col2Key]

# <markdowncell>

# Read in ALL rows of data from the Google Spreadsheet, but filter out columns that are not listed in `fieldnames`.

# <codecell>

filtered_data = []
for row in worksheet.get_all_records():
    filtered_data.append({k:v for k,v in row.iteritems() if k in fieldnames})
#    print "Number of rows: {}".format(len(filtered_data))

# <markdowncell>

# Use the convenience function `take()` to print out only 3 lines from the filtered_data.

# <codecell>

#for row in take(3, filtered_data):
#    print row



# What is your learning style col
# get all the scores for the 4 categories 
# () represents empty scores
def getRowLearn():
	dictScore = {}
	i = 0
	for row in filtered_data:
		lsScore = []
		strLearn = row[col1Key]
		splittedWords = strLearn.split()
		lsScore+= [int(word) for word in splittedWords if word.isdigit()]
		dictScore[i] = lsScore
		i+=1
	return dictScore

# store each of the category into a list
dtscore = getRowLearn()
lsVisual = []
lsAural = []
lsReadW = []
lsKines = []
for item in dtscore.values():
	if(item == []):
		lsVisual += [()]
		lsAural += [()]
		lsReadW += [()]
		lsKines += [()]
	else:
		lsVisual += [item[0]]
		lsAural += [item[1]]
		lsReadW += [item[2]]
		lsKines += [item[3]]
'''
>>> lsVisual
[(), 3, (), 0, 9, (), 8, 8, (), 13, 10, (), 15, (), 5, 3, (), 10, 4, 4, 11, 4, 9, 10, (), 9, 7, (), (), 6, 6, 5, 11, (), 12, (), (), 2, 1, (), 9, (), (), (), 9, 9, 7, 2]
>>> len(lsVisual)
48
>>> lsAural
[(), 5, (), 10, 9, (), 7, 1, (), 10, 4, (), 9, (), 1, 6, (), 10, 3, 3, 11, 4, 7, 7, (), 8, 11, (), (), 4, 5, 3, 11, (), 10, (), (), 3, 4, (), 7, (), (), (), 10, 11, 8, 6]
>>> lsReadW
[(), 4, (), 14, 3, (), 8, 8, (), 8, 5, (), 6, (), 4, 6, (), 2, 1, 11, 6, 7, 10, 11, (), 10, 4, (), (), 7, 7, 9, 9, (), 13, (), (), 6, 4, (), 5, (), (), (), 10, 3, 9, 4]
>>> lsKines
[(), 7, (), 5, 3, (), 5, 5, (), 11, 10, (), 11, (), 6, 7, (), 13, 8, 4, 9, 1, 12, 7, (), 11, 8, (), (), 5, 5, 6, 5, (), 10, (), (), 5, 7, (), 5, (), (), (), 9, 8, 10, 4]
'''

# clear all the empty tuples
lsVisual1 = []
lsAural1 = []
lsReadW1 = []
lsKines1 = []

lsVisual1 = [i for i in lsVisual if i!=()]
lsAural1 = [i for i in lsAural if i!=()]
lsReadW1 = [i for i in lsReadW if i!=()]
lsKines1 = [i for i in lsKines if i!=()]

# get index of empty learning style score
def getEmptIndex():
	emptyScoreIndex = []
	for i in range (0,len(lsVisual)):
		if(lsVisual[i]==()):
			emptyScoreIndex += [i]
	return emptyScoreIndex


# 
def getRowProduce():
	dtFreq = {}
	i = 0
	for row in filtered_data:
		strProd = row[col2Key]
		dtFreq[i] = strProd
		i += 1
	return dtFreq

dtproduce = getRowProduce()

# just get all the rows in dtproduce that have learning score
# save the result into a list
emptyScoreIndex = getEmptIndex()
lsProduce = []
for i in dtproduce:
	if i not in emptyScoreIndex:
		lsProduce += [dtproduce[i]]

# check length
len(lsVisual1)
len(lsAural1)
len(lsReadW1)
len(lsKines1)
len(lsProduce)
# length ok, they are all 31 now

# 
lsSometimes = []
lsOften = []
lsNotOften = []
lsAlways = []
countSome = 0
countOften = 0
countNotOft = 0
countAl = 0
for item in lsProduce:
	inSome = 0
	inOf = 0
	inNotOf = 0
	inAl = 0

	if(item == "Sometimes"):
		inSome = 1
		countSome += 1
	if(item == "Often"):
		inOf = 1
		countOften += 1
	if(item == "Not Often"):
		inNotOf = 1
		countNotOft += 1
	if(item == "Always"):
		inAl = 1
		countAl += 1

	lsSometimes += [inSome]
	lsOften += [inOf]
	lsNotOften += [inNotOf]
	lsAlways += [inAl]

# get row index number for each category
indSometimes = []
indOften = []
indNotOften = []
indAlways = []

for i in range(0, len(lsSometimes)):
	if(lsSometimes[i]):
		indSometimes += [i]
	if(lsOften[i]):
		indOften += [i]
	if(lsNotOften[i]):
		indNotOften += [i]
	if(lsAlways[i]):
		indAlways += [i]


# calculate the mean score for each visual/aural/readwrite/kinesthetic
# for each sometimes/often/notoften/always

#get the corresponding score according to the index number for sometimes/often/notoften/always
AlwaysVisual = []
AlwaysAural = []
AlwaysReadW = []
AlwaysKines = []
for index in indAlways:
	AlwaysVisual += [lsVisual1[index]]
	AlwaysAural += [lsAural1[index]]
	AlwaysReadW += [lsReadW1[index]]
	AlwaysKines += [lsKines1[index]]

meanAlwaysV = sum(AlwaysVisual) / len(AlwaysVisual)
meanAlwaysA = sum(AlwaysAural) / len(AlwaysAural)
meanAlwaysR = sum(AlwaysReadW) / len(AlwaysReadW)
meanAlwaysK = sum(AlwaysKines) / len(AlwaysKines)


sometimesVisual = []
sometimesAural = []
sometimesReadW = []
sometimesKines = []
for index in indSometimes:
	sometimesVisual += [lsVisual1[index]]
	sometimesAural += [lsAural1[index]]
	sometimesReadW += [lsReadW1[index]]
	sometimesKines += [lsKines1[index]]

meanSomeV = sum(sometimesVisual) / len(sometimesVisual)
meanSomeA = sum(sometimesAural) / len(sometimesAural)
meanSomeR = sum(sometimesReadW) / len(sometimesReadW)
meanSomeK = sum(sometimesKines) / len(sometimesKines)


oftenVisual = []
oftenAural = []
oftenReadW = []
oftenKines = []
for index in indOften:
	oftenVisual += [lsVisual1[index]]
	oftenAural += [lsAural1[index]]
	oftenReadW += [lsReadW1[index]]
	oftenKines += [lsKines1[index]]

meanOftenV = sum(oftenVisual) / len(oftenVisual)
meanOftenA = sum(oftenAural) / len(oftenAural)
meanOftenR = sum(oftenReadW) / len(oftenReadW)
meanOftenK = sum(oftenKines) / len(oftenKines)


NotofVisual = []
NotofAural = []
NotofReadW = []
NotofKines = []
for index in indOften:
	NotofVisual += [lsVisual1[index]]
	NotofAural += [lsAural1[index]]
	NotofReadW += [lsReadW1[index]]
	NotofKines += [lsKines1[index]]

meanNotOftenV = sum(NotofVisual) / len(NotofVisual)
meanNotOftenA = sum(NotofAural) / len(NotofAural)
meanNotOftenR = sum(NotofReadW) / len(NotofReadW)
meanNotOftenK = sum(NotofKines) / len(NotofKines)


# plot graphs
import matplotlib
#%matplotlib inline
#%load_ext rmagic

import numpy as np
import matplotlib.pyplot as plt

# Below is the bar chart of Learning style scores in terms of 
# frequencies being a producer in the group.
N = 4
ind = np.arange(N)
width = 0.2

vMeans = [meanAlwaysV, meanSomeV, meanOftenV, meanNotOftenV]
aMeans = [meanAlwaysA, meanSomeA, meanOftenA, meanNotOftenA]
rMeans = [meanAlwaysR, meanSomeR, meanOftenR, meanNotOftenR]
kMeans = [meanAlwaysK, meanSomeK, meanOftenK, meanNotOftenK]

fig, ax = plt.subplots()

vColor = '#8A89A6'
aColor = '#7B6888'
rColor = '#6B486B'
kColor = '#A05d56'

#vColor = '#FFFF66'
#aColor = '#FFBF00'
#rColor = '#2ECCFA'
#kColor = '#5882FA'

rects1 = ax.bar(ind, vMeans, width, color = vColor)
rects2 = ax.bar(ind+width, aMeans, width, color=aColor)
rects3 = ax.bar(ind+2*width, rMeans, width, color=rColor)
rects4 = ax.bar(ind+3*width, kMeans, width, color=kColor)

ax.set_ylabel('Scores')
ax.set_xlabel('Being producer in the group')
ax.set_title('Learning style scores in terms of frequencies of being producer in the group')
ax.set_xticks(ind+2*width)
ax.set_xticklabels(('Always', 'Sometimes', 'Often', 'Not Often'))
ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('Visual', 'Aural', 'Read/Write', 'kinesthetic'))
plt.yticks(np.arange(0,15,1))
plt.show()







