


'''
> Your introduction should also include identifying information (your name, date, etc.)
    Gabriel Chambers
    4/13/2020

I use the following features: all bigrams that appear in tweet (sentence). 
each bigram is tagged with "negative" or "psotive" after all tweets have been checked
and the associated sentiment for the bigram is assigned by frequency,
and a certainty value is applied by calculating log likelihood.

scorer.py output:

Accuracy: 0.75

Confusion Matrix, where outer key is my calculated data and the inner keys are the line-key.txt values
For example:
        negative: {'positive': 4, 'negative': 44}
Can be read as: What my program thought was a negative was correctly tagged 44 times,
but 4 times it was actually supposed to be a positive

positive: {'positive': 68, 'negative': 10}
negative: {'positive': 4, 'negative': 44}


"And compare your results to that of the most frequeant sense baseline":
i think that is asking for this:
most freuqnt sense is positive
accuracy for positive is 68/78=.87179487179




1) describe the problem to be solved well enough so that someone not
familiar with our class could understand:

find the sentiment of asentence. This means decern wether a sentence carries a positive or negative weight or
association based on the words used.



 2) give actual examples of program input and output, along with usage instructions, 

input:

file called sentiment-test.txt with:
<corpus lang="en">
<lexelt item="sentiment">
<instance id="620979391984566272">
<context>
On another note, it seems Greek PM Tsipras married Angela Merkel to Francois Hollande on Sunday #happilyeverafter http://t.co/gTKDxivf79
</context>
</instance>
<instance id="621340584804888578">
<context>
Amazon Prime Day is just like Black Friday if you only buy bulk protein powder and will-making software on Black Friday.
</context>
</instance>
...

file called sentiment-train.txt with:
<corpus lang="en">
<lexelt item="sentiment">
<instance id="620821002390339585">
<answer instance="620821002390339585" sentiment="negative"/>
<context>
Does @macleansmag still believe that Ms. Angela Merkel is the "real leader of the free world"?  http://t.co/isQfoIcod0 (Greeks may disagree
</context>
</instance>
<instance id="621090050848198657">
<answer instance="621090050848198657" sentiment="negative"/>
<context>
...


output:
printed to stdout:
<answer instance="620979391984566272" sentiment="negative"/>
<answer instance="621340584804888578" sentiment="positive"/>
...


usage instrictions:

run like: python3 sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt
where my-model.txt will be for troubleshooting and shows the data structure constructed



 3) describe the algorithm you have used to solve the problem, specified in a stepwise or point by point fashion. 

take in the training and testing info. First refine training file
splice out the answer and the actual setence for each sentence in the training info.
Turn the test of the sentence into bigrams.
Create a dictionary of all bigrams, whos values is another dictionary containing a counter
for how many times that bigram is seen in a negative seintiment vs how many times it is seen
with a positive sentiment.
Next, the dictionary is looped through and a certainty value is calculated for each bigram
based on the sentiment with the highest frequency for that bigram using log-likelihood.

Next the testing data is refined. The Instance number and the test context is extracted.
The text of each entry is broken up into all bigrams accociated with each instance number.
Then each sentence is looped through.
Within each sentence, each bigram is compared to the dictionary built from the training data.
If a bigram corresponds to one in the dictionary, the certainty value of that bigram is added
to a counter for it's corresponding sentiment.
Once every bigram has been checked, the higher of the two counters (positive sentiment certainty
vs negative sentiment certainty) dictates whether the sentence is tagged as positive or negative.
If for some reason the counters are equal (perhaps if no bigrams were seen in the training data),
then the tweet is tagged as positive because there are more positive tweets in the training info.
Finally the instance number is joined with the calculated sentiment, and printed in a format to
match the key.





"2) Detailed comments throughout code that fully explain details of algorithm.
Implementation must work as described and solve problem correctly to get credit for
detailed comments."
'''



import math
import os
import re
import sys


# prints lists prettier for testing purposes
def printlist(lst):
    for e in lst:
        print(e)


# reads in a file and returns a string
def readIn(fn):
    with open(fn, 'r+') as f:
        lines = []
        for line in f:
            lines.append(line.strip().lower())
        return ' '.join(lines)


# splits a string at instances of another string
# in (string, string)
# out: list
def extractSplit(str, term):
    lsts = str.split(term)
    return lsts


# extracts only a substring from a string which matches a regex
# in: (string, string), where second string is a regex
# out: string
def extractRegex(str, term):
    if re.search(term, str) is not None:
        rtn = re.search(term, str)
        return rtn.group(1)
    return


# takes in a list of strings and strips out unneeded parts using regex
# in: (list: [string])
# out: list: [string]
def stripContextExtras(lst):
    newlst = []
    for text in lst:
        text = re.sub(r"http[^\s]*", '', text)
        text = re.sub(r"'s", 's', text)
        text = re.sub(r"n't", 'nt', text)
        text = re.sub(r"i'm", 'im', text)
        text = re.sub(r'</', '<', text)
        text = ' '.join(text.split(r'<s>'))
        text = ' '.join(text.split(r'<p>'))
        text = ' '.join(text.split(r'<@>'))
        text = re.sub(r'[^a-zA-Z\d\s<>@#]', ' ', text)  # remove all non alphanumeric, whitespace, and elbow brackets
        text = re.sub(r'@[^\s]*', '@user', text)  # change @usertags to all be @user so there can be more consistency
        text = ' '.join(text.split())
        newlst.append(text)
    return newlst


# takes in string of many words.
# outputs list of all bigram tuples in the string
# input: "This is a sentence".
# output: [(This, is), (is, a), (a, sentence)]
def sentenceToBigramList(sntnc):
    sntnc = sntnc.split()
    bigrams = []
    prev_word = ''
    for word in sntnc:
        if prev_word != '':
            bigrams.append((prev_word, word))
        prev_word = word
    return bigrams


# combines two lists of equal size index by index. returns list of sublists which contains
# the entry of both input lists at current index
# in:(list: [any], list: [any])
# out: #out: list: [list: [any]]
def combine(lst1, lst2):
    outlst = []
    for index in range(len(lst1)):
        innerlst = []
        innerlst.append(lst1[index])
        innerlst.append(lst2[index])
        outlst.append(innerlst)
    return outlst


# takes as input the output of above function, combines(l1,l2), and outputs a nested dictionary in form:
# tdict = {(w1, w2) :{'positive': n
#                       'negative': n
#                       'certainty': 0},
#          (w2, w3) :{'positive': n
#                       'negative': n
#                       'certainty': 0},
#          ...
#          }
#
# in: (list: [list: [any]])
# out: dictionary in above form
#
# now attempting normalizing to make up for uneven input (second half of method)
def createTrainingDict(ContextSense):
    tdict = {}
    pcounter = 0
    ncounter = 0
    for entries in ContextSense:
        context = entries[0]
        sentiment = entries[1]
        for bigram in context:
            if bigram not in tdict:
                tdict[bigram] = {'positive': 0,
                                 'negative': 0,
                                 'certainty': 0}
            tdict[bigram][sentiment] += 1
            if sentiment == 'positive':
                pcounter += 1
            elif sentiment == 'negative':
                ncounter += 1


    # attempted normalization: didnt end up working. commenting out but keeping around in case i think of better way to impliment
    '''
    if pcounter > ncounter:
        pdict = {}
        for bgram, sentiment in tdict.items():
            pdict[bgram] = {'positive': sentiment['positive'],
                            'negative': round(sentiment['negative'] * (pcounter / ncounter)),
                            'certainty': 0}
        tdict = pdict
    elif ncounter > pcounter:
        ndict = {}
        for bgram, sentiment in tdict.items():
            ndict[bgram] = {'positive': round(sentiment['positive'] * (ncounter / pcounter)),
                            'negative': sentiment['negative'],
                            'certainty': 0}
        tdict = ndict
    '''
    ######END attempted normalization, made it overall less accurate but increased "negative" accuracy. might need to delete this chunk

    return tdict


# takes the training table with number of occurances and finds the corresponding certainty value
def toCertaintyTable(tdict):
    for bigram, sentiments in tdict.items():
        sentiments['certainty'] = findCertainty(sentiments['positive'], sentiments['negative'])
        if sentiments['negative'] <= sentiments['positive']:
            del sentiments['negative']
        else:
            del sentiments['positive']
    return tdict


# finds certainty value given two inputs using formula given in slides
# in: (int, int)
# out: float
def findCertainty(positive, negative):
    if (positive == 0) and (negative == 0):
        return 0
    elif (positive == 0) or (negative == 0):
        return 4
    return abs(math.log((positive / (positive + negative)) / (negative / (positive + negative))))


# writes training dictionary in readable format to a file for debugging
# in: filename as string
# out: nothing. prints inside
def printToMyModel(filename, dic):
    modelfile = open(filename, "w")

    for bigram, sentiments in dic.items():
        modelfile.write('feature: ')
        for word in bigram:
            modelfile.write(word)
            modelfile.write(' ')
        modelfile.write('\n')
        for sentiment_name, sentiment_value in sentiments.items():
            modelfile.write(sentiment_name)
            modelfile.write(': ')
            modelfile.write(str(sentiment_value))
            modelfile.write('\n')
        modelfile.write('\n')

    modelfile.close()  # to change file access modes
    return


# takes the training dict and the list of test instances paired with the bigrams
# finds sentiment for test based off the training dictionary
# by testing every bigram against dictionary and making a sum of negative certainties
# enountered vs positive certainties
# then choosing the sentiment with the highest sum of certainties for all bigrams in the sentence
# output in form: list [instance#, list of bigrams, sentiment,
# #       positve sentiment certainty sum, negative sentiment certainty sum]
def findTestSolutions(traind, testIB):
    testIBS = []  # Insantance, Bigram, Sentiment not Internal Bowel Syndrome
    for tweet in testIB:
        instance = tweet[0]
        sentence = tweet[1]
        positive_sum = 0.0
        negative_sum = 0.0
        for bigram in sentence:
            if bigram in traind:
                if 'positive' in traind[bigram] and traind[bigram]['certainty'] != 0:
                    positive_sum += traind[bigram]['certainty']
                elif traind[bigram]['certainty'] != 0:
                    negative_sum += traind[bigram]['certainty']
        if positive_sum >= negative_sum:
            answer = 'positive'
        else:
            answer = 'negative'
        testIBS.append([instance, sentence, answer, positive_sum, negative_sum])
    return testIBS


def toformatoutput(testsol):
    formatted = []
    for tweet in testsol:
        formatted.append('<answer instance="' + tweet[0] + '" sentiment="' + tweet[2] + '"/>')
    return formatted

##############################################PROGRAM START#############################################
pythonFileName = sys.argv.pop(0)
linetrain = sys.argv.pop(0)
linetest = sys.argv.pop(0)
mymodel = sys.argv.pop(0)
trainText = readIn(linetrain)
testText = readIn(linetest)

# extract the info needed from trainText.
trainTerms = extractSplit(trainText, '</instance>')
trainTerms.pop(-1)  # pops a 'None' that can cause problems later
trainInstance = []
trainSentiment = []
trainContext = []
for term in trainTerms:
    # regex: match exactly "<instance ~any characters until first '>'~"
    trainInstance.append(extractRegex(term, r'.*?<instance id="(.*)">'))
    trainSentiment.append(extractRegex(term, r'.*?sentiment="(.*[^"])"\/>'))  # regex same as above but w "answer"
    trainContext.append(extractRegex(term, r'<context>(.*?)<\/context>'))  # group everything between context tags
trainContext = stripContextExtras(trainContext)

# turn trainContext to list of bigram tuples instead of long string
# in form [(w1, w2), (w2, w3), ... (Wn-1, Wn)]
trainBigrams = []
for sentence in trainContext:
    trainBigrams.append(sentenceToBigramList(sentence))

# combine the two context and answer lists together so you know if a given context corresponds to positive or negative
# in form [[(w1, w2), (w2, w3), ... (Wn-1, Wn)], sense]
trainContextSentiment = combine(trainBigrams, trainSentiment)

# build dictionary of training data in form dict{featuretype: {feature: {sense: numOccurances}}}
# where feature is a tuple containing 1 to 2 words
trainingDict = createTrainingDict(trainContextSentiment)
# calculates the certainty value of each tuple entry
trainingDict = toCertaintyTable(trainingDict)

# print training dict to model
printToMyModel(mymodel, trainingDict)

# parse testing data::
# extract the info needed from testText.
testTerms = extractSplit(testText, '</instance>')
testTerms.pop(-1)  # pops a 'None' that can cause problems later
testInstance = []
testContext = []
for term in testTerms:
    # regex: match exactly "<instance ~any characters until first '>'~"
    testInstance.append(extractRegex(term, r'.*?<instance id="(.*)">'))
    testContext.append(extractRegex(term, r'<context>(.*?)<\/context>'))  # group everything between context tags
testContext = stripContextExtras(testContext)
# turn testContext to list of bigram tuples instead of long string
# in form [(w1, w2), (w2, w3), ... (Wn-1, Wn)]
testBigrams = []
for sentence in testContext:
    testBigrams.append(sentenceToBigramList(sentence))
# combine the two context and Instance lists together so you can
# in form [[(w1, w2), (w2, w3), ... (Wn-1, Wn)], sense]
testInstanceBigrams = combine(testInstance, testBigrams)

# compare data against training dictionary and find solution:
# option 1: pick single highest bigram certainty other
# option 2: make sum of positive certainties and negative certainties and compare them. whichever sum higher is
# assigned
testSolutions = findTestSolutions(trainingDict, testInstanceBigrams)  # i used option 2. made more sense
# testSolutions list in format: list [instance#, list of bigrams, sentiment,
#       positve sentiment certainty sum, negative sentiment certainty sum]


# 3) construct output in form of sentiment-test-key.txt
formatted_solution = toformatoutput(testSolutions)
printlist(formatted_solution)



#####TESTING######
# printlist(trainInstance)
# printlist(trainSentiment)
# printlist(trainContext)
# printlist(trainContextSentiment)
# print(trainingDict)
# printlist(testInstance)
# printlist(testContext)
# printlist(testBigrams)
# printlist(testInstanceBigrams)
# printlist(testSolutions)
#####END TEST#####
