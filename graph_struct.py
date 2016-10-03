##################################################################
# Stores Graph structure classes and functions related to Graph
import decimal

class GraphNode():
    "Graph Node structure for each word"

    def __init__(self, word):
        self.word = word
        self.used = False
        self.nextList = []

    def addNext(self, next):
        self.nextList.append(next)

    def probNext(self, nextWord):
        next_prob = 0
        for nextNode in self.nextList:
            if nextNode.after.wordStr == nextWord:
                next_prob = nextNode.prob
        return next_prob


class NextNode():
    "Node structure which contains prev, after and probability"

    def __init__(self, after, prob):
        self.after = after
        self.visited = False
        self.prob = prob


class Word():
    "Word structure containing word and type"

    def __init__(self, wordStr, type):
        self.wordStr = wordStr
        self.type = type


#################################################################

# for storing queue structure
class QueueEntry:
    def __init__(self, wordKey, parents):
        self.wordKey = wordKey
        self.parents = parents

    def generateSentence(self):
        sentence = [self.wordKey]
        if self.parents:
            sentence = self.parents + sentence
        sentenceStr= " ".join(str(y) for y in sentence)
        # print("sentence_so_far(" + str(len(sentence)) + " words): [ " + sentenceStr + "]")
        return sentence

#################################################################

# Graph Functions
###################################################################
###################################################################
# Parse the text and generate appropriate graph (dictionary structure) for words
# Read from input.text (MAY BE CHANGED LATER)
# input:
def parseGraph(fileName):
    f = open(fileName, 'r')
    graph = dict()
    for line in f.readlines():
        wlist = line.split('//')
        word1list = wlist[0].split('/')
        word2list = wlist[1].split('/')
        prob = decimal.Decimal(wlist[2])

        # generate word
        word1 = Word(word1list[0], word1list[1])
        word2 = Word(word2list[0], word2list[1])

        afternode = NextNode(word2, prob)

        graphKey = word1.wordStr + "-" + word1.type

        if graphKey in graph:
            thisnode = graph[graphKey]
            thisnode.addNext(afternode)
            graph[graphKey] = thisnode
        else:
            thisnode = GraphNode(word1)
            thisnode.addNext(afternode)
            graph[graphKey] = thisnode

    return graph


# Print Graph
# Note: this will not be used in actual function
def printGraph(graph):
    print("---------------------------Print Graph----------------------------")
    for word, node in graph.items():
        toprint = word
        afterstring = "{"
        for nextNode in node.nextList:
            afterstring = afterstring + "(" + nextNode.after.wordStr + "[" + nextNode.after.type + "] ," + str(nextNode.prob) + ")"
            afterstring += ", "
        afterstring += "}"
        toprint = toprint + " : " + afterstring
        print(toprint)
        print("\n")
    print("------------------End of Print Graph -----------------------------")