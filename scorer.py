'''
run with: python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt
'''

import sys, re

#reads in a file and returns list of lines
def readIn(fn):
    with open(fn, 'r+') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        return lines
    return None

#takes two lists and returns decimal value of how accurate actual vs expect is
def compareAccuracy(actual, expected):
    same = 0
    total = 0
    for index in range(len(actual)):
        total += 1
        if actual[index] == expected[index]:
            same+=1
    return same/total



#extracts fronm a string using a regex
def extractRegex(str, term):
    if re.search(term, str) is not None:
        rtn = re.search(term, str)
        return rtn.group(1)
    return


##extracts fronm a list of string using a regex
def extractSentiment(inlst):
    ##extract 'positive' or 'negative' from trainAnswer
    rtnlst = []
    for term in inlst:
        rtnlst.append(extractRegex(term, r'sentiment="(.*?)"'))
    return rtnlst


#creates emptyconfusion matrix
def initializeMatrix():
    matrix = {
                'positive': {
                            'positive': 0,
                            'negative': 0
                },
                'negative': {
                            'positive': 0,
                            'negative': 0
                }
    }
    return matrix


#fills in the confusion matrix and calls the initializer
#mine and lkey are each single lists: [positive, positive, negative, positive...]
def buildMatrix(mans, lkey):
    matrix = initializeMatrix()
    for index in range(len(mans)):
        matrix[mans[index]][lkey[index]] += 1
    return matrix


#prints readably
def printPretty(matrix):
    print('Confusion Matrix, where outer key is my calculated data and the inner keys are the line-key.txt values')
    print('For example:')
    print("        negative: {'positive': 4, 'negative': 44}")
    print('Can be read as: What my program thought was a negative was correctly tagged 44 times,')
    print('but 4 times it was actually supposed to be a positive', end='\n\n')
    for actualpos, expecteddict in matrix.items():
        print(actualpos, end=': ')
        print(expecteddict)
    return



#####START PROGRAM#######
pythonFileName = sys.argv.pop(0)
myansf = sys.argv.pop(0)
linekeyf = sys.argv.pop(0)

myans = readIn(myansf)
linekey = readIn(linekeyf)

print('Accuracy: ' + str(compareAccuracy(myans, linekey)), end='\n\n')#prints accuracy

myans = extractSentiment(myans)
linekey = extractSentiment(linekey)

#makes matrix
confusionMatrix = buildMatrix(myans, linekey)

printPretty(confusionMatrix)