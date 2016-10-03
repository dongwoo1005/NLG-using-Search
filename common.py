# Stores commonly used functions for A1
import decimal


##################################################################
##################################################################
# isValidSentence: checks if the given sentence is valid with given sentence Spec
# mayFormValidSentence: checks if the given sentence(words) has valid structure so far
# inputs:
#   s: list of Words to check
#   sentenceSpec: format of valid sentence
#   graph: parsed graph structure to check the word's type
def isValidSentence(s, sentenceSpec):
    numReqParts = len(sentenceSpec)
    numParts = len(s)
    if numReqParts != numParts:
        return False

    isSpecSatisfied = True
    for x in range(0, numParts):
        thisWord = s[x].split('-')
        thisType = thisWord[1]
        if thisType != sentenceSpec[x] :
            isSpecSatisfied = False
            break

    return isSpecSatisfied


###################################################################
def mayFormValidSentence(s, sentenceSpec):
    numReqParts = len(sentenceSpec)
    numParts = len(s)
    if numReqParts < numParts:
        return False

    isSpecSatisfied = True
    for x in range(0, numParts):
        thisWord = s[x].split('-')
        thisType = thisWord[1]
        if thisType != sentenceSpec[x] :
            isSpecSatisfied = False
            break
    return isSpecSatisfied


############################################################
############################################################
# calculate probability of given sentence s
def calculateProb(s, graph) :
    sentence_len = len(s)
    init_word =s[0]
    prob = decimal.Decimal(1)
    for i in range(0, sentence_len):
        dest_word = s[i]
        this_prob = 1
        if init_word == dest_word:
            this_prob = 1
        else:
            origin = graph[init_word]
            dest_wordStr = dest_word.split('-')[0]
            this_prob = origin.probNext(dest_wordStr)
        prob = prob * this_prob
        init_word = s[i]
    return prob


############################################################
# convert the list of sentences to string
# s contais the list of "word-type" pair in sequence
def makeString(s):
    sLen = len(s)
    sentence = ""
    for x in range(0, sLen):
        word = s[x].split("-")
        sentence += word[0]
        if x != sLen -1:
            sentence += " "
    return sentence
