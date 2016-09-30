# example string from input (for test): there/EX//was/VBD//0.21311475409836064
# for A1P1, valid sentence structure is: "NNP", "VBD", "DT", "NN"

################################################################3
# global variables
p1struct=["NNP", "VBD", "DT", "NN"]

##################################################################

class GraphNode() :
    "Graph Node structure for each word"
    def __init__(self, word):
        self.word = word
        self.nextList = []

    def addNext(self, next):
        self.nextList.append(next)

class NextNode():
    "Node structure which contains prev, after and probability"
    def __init__(self, after, prob):
        self.after = after
        self.prob = prob

class Word():
    "Word structure containing word and type"
    def __init__(self, wordStr, type):
         self.wordStr = wordStr
         self.type = type

##################################################################
def isValidSentence(s, sentenceSpec, graph):
    #s = list of Word
    # wordDic = dictionary of word generated based on input.txt
    numReqParts = len(sentenceSpec)
    numParts = len(s)
    if numReqParts > numParts:
        return False

    isSpecSatisfied = True
    for x in range(0, numParts):
        thisWord = s[x]
        gword = graph[thisWord]
        if gword.word.type != sentenceSpec[x]:
            isSpecSatisfied = False
            return False

    return isSpecSatisfied

##################################################################
def mayFormValidSentence(s, sentenceSpec, graph):
    numReqParts = len(sentenceSpec)
    numParts = len(s)
    if numReqParts < numParts:
        return False

    isSpecSatisfied = True
    for x in range(0, numParts):
        thisWord = s[x]
        gword = graph[thisWord]
        if gword.word.type != sentenceSpec[x]:
            isSpecSatisfied = False
            return False
    return isSpecSatisfied


#########################################################
# Parse the text and generate appropriate graph for words
# Read from input.text (MAY BE CHANGED LATER)
# input:
def parseGraph(fileName):
    f = open(fileName, 'r')
    graph = dict()
    for line in f.readlines():
        # do something...
        wlist = line.split('//')
        word1list = wlist[0].split('/')
        word2list = wlist[1].split('/')
        prov = wlist[2]

        # generate word
        word1 = Word(word1list[0], word1list[1])
        word2 = Word(word2list[0], word2list[1])

        afternode = NextNode(word2, prov)

        if word1.wordStr in graph:
            thisnode = graph[word1.wordStr]
            thisnode.addNext(afternode)
            graph[word1.wordStr] = thisnode
        else:
            thisnode = GraphNode(word1)
            thisnode.addNext(afternode)
            graph[word1.wordStr] = thisnode

    return graph


# Print Graph
# Note: this will not be used in actual function
def printGraph(graph):
    for word, node in graph.items():
        toprint = word + "[" + node.word.type + "]"
        afterstring = "{"
        for nextNode in node.nextList :
            afterstring = afterstring + "(" + nextNode.after.wordStr + "[" + nextNode.after.type + "] ," + nextNode.prob + ")"
            afterstring += ", "
        afterstring +="}"
        toprint = toprint + " - " + afterstring
        print(toprint)



############################################################
# main function that generates sentence using BFS
def generate(startingWord, sentenceSpec, graph):
    sentence_so_far = []
    temp_sentence = []

    # parse graph from given file
    g = parseGraph(graph)
    print("# of items in Graph: " + str(len(g)))
    printGraph(g)


    issentenceyet = isValidSentence(sentence_so_far, sentenceSpec, g)
    print(issentenceyet)

    # do bst




generate("benjamin", p1struct, "input.txt")