

#############################################################################################################
'''                                            OVERVIEW

> Your introduction should also include identifying information (your name, date, etc.)
    Gabriel Chambers
    4/13/2020

1) describe the problem to be solved well enough so that someone not
familiar with our class could understand:

given input in the form of text documents from two files, descern how accurately the text documents match line by line
and create a confusion matrix.
From https://en.wikipedia.org/wiki/Confusion_matrix:
"In the field of machine learning and specifically the problem of statistical classification, a confusion matrix, 
also known as an error matrix,[6] is a specific table layout that allows visualization of the performance of an algorithm, 
typically a supervised learning one (in unsupervised learning it is usually called a matching matrix). Each row of the matrix 
represents the instances in a predicted class while each column represents the instances in an actual class (or vice versa).[2] 
The name stems from the fact that it makes it easy to see if the system is confusing two classes (i.e. commonly mislabeling one as another)."




2) give actual examples of program input and output, along with usage instructions, 

input:
a text file, call it my-line-answers.txt, in form: 
<answer instance="line-n.w8_059:8174:" sentiment="positive"/>
<answer instance="line-n.w7_098:12684:" sentiment="positive"/>
<answer instance="line-n.w8_106:13309:" sentiment="positive"/>
...



a text file, call it line-key.txt, in form: 
<answer instance="line-n.w8_059:8174:" sentiment="positive"/>
<answer instance="line-n.w7_098:12684:" sentiment="positive"/>
<answer instance="line-n.w8_106:13309:" sentiment="positive"/>
...

ex output:

Accuracy: 0.75

Confusion Matrix, where outer key is my calculated data and the inner keys are the line-key.txt values
For example:
        negative: {'positive': 4, 'negative': 44}
Can be read as: What my program thought was a negative was correctly tagged 44 times,
but 4 times it was actually supposed to be a positive

positive: {'positive': 68, 'negative': 10}
negative: {'positive': 4, 'negative': 44}



usage instructions:

run with: python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt

car1.setdaemin(true)
car2.setdaemin(true)
car1.start()
car2.start()

 3) describe the algorithm you have used to solve the problem, specified in a stepwise or point by point fashion. 

I read in the files as a list line per line
I went through a loop with both lists and added one for each identical entry at the same index, then divided by the size of the lists and print it

Then i extracted the keyword that matters in each list, positive and negative, and created a list of just those
Then I made the confusion matrix
Then i printed it


'''
#############################################################################################################

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

#prints the output to STDOUT
printPretty(confusionMatrix)