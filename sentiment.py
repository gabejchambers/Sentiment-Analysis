'''
run with:
python3 sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt
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
        text = re.sub(r'[^a-zA-Z\d\s:<>@#]', ' ', text)  # remove all non alphanumeric, whitespace, and elbow brackets
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

# combine the two context and answer lists together so you know if a given context corresponds to phone or product
# in form [[(w1, w2), (w2, w3), ... (Wn-1, Wn)], sense]
trainContextAnswer = combine(trainBigrams, trainSentiment)

#####TESTING######
printlist(trainInstance)
printlist(trainSentiment)
printlist(trainContext)
printlist(trainContextAnswer)
#####END TEST#####
