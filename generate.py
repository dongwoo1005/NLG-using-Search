# example string from input (for test): there/EX//was/VBD//0.21311475409836064
# for A1P1, valid sentence structure is: "NNP", "VBD", "DT", "NN"
import queue

################################################################3
# global variables
p1struct = ["NNP", "VBD", "DT", "NN"]


##################################################################

class GraphNode():
    "Graph Node structure for each word"

    def __init__(self, word):
        self.word = word
        self.used = False
        self.nextList = []

    def addNext(self, next):
        self.nextList.append(next)

    def probNext(self, nextWord):
        for nextNode in self.nextList:
            if nextNode.after.wordStr == nextWord:
                return nextNode.prob
        return 0


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


##################################################################
##################################################################
# isValidSentence: checks if the given sentence is valid with given sentence Spec
# mayFormValidSentence: checks if the given sentence(words) has valid structure so far
# inputs:
#   s: list of Words to check
#   sentenceSpec: format of valid sentence
#   graph: parsed graph structure to check the word's type
def isValidSentence(s, sentenceSpec, graph):
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
        for nextNode in node.nextList:
            afterstring = afterstring + "(" + nextNode.after.wordStr + "[" + nextNode.after.type + "] ," + nextNode.prob + ")"
            afterstring += ", "
        afterstring += "}"
        toprint = toprint + " - " + afterstring
        print(toprint)


############################################################
############################################################
# calculate probability of given sentence s
# todo: fix this !!
def calculateProb(s, graph) :
    sentence_len = len(s)
    init_word = s[0]
    prob = 1
    for i in range(0, sentence_len):
        dest_word = s[i]
        this_prob = 1
        if init_word == dest_word:
            this_prob = 1
        else:
            origin = graph[init_word]
            this_prob = origin.probNext(dest_word)
        prob = prob * this_prob
    return prob

############################################################
############################################################
# main function that generates sentence using BFS
def generate(startingWord, sentenceSpec, graph):
    sentence_so_far = []
    highest_prob_sentence = []
    prob = float(0)

    # parse graph from given file
    g = parseGraph(graph)
    print("# of items in Graph: " + str(len(g)))
    printGraph(g)

    issentenceyet = isValidSentence(sentence_so_far, sentenceSpec, g)
    print(issentenceyet)

    # do bst
    node_visited = queue.Queue()  # FIFO queue
    node_count = 0

    # init = g[startingWord]
    # print(init.word.wordStr + "[" + init.word.type + "] - childrens: " + str(len(init.nextList)))
    node_visited.put(startingWord)

    while not node_visited.empty():
        this_word = node_visited.get()
        if this_word in g:
            sentence_so_far.append(this_word)
            this_node = g[this_word]
            node_count += 1

            # todo: check if it is sentence and if it may be sentence.
            is_sentence = isValidSentence(sentence_so_far, sentenceSpec, g)
            if __name__ == '__main__':
                if is_sentence:
                    # update the sentence that has highest probability
                    this_prob = calculateProb(sentence_so_far, g)
                    print("this_prob: " + this_prob)

                    if this_prob > prob:
                        prob = this_prob
                        highest_prob_sentence = sentence_so_far
                else:
                    may_sentence = mayFormValidSentence(sentence_so_far, sentenceSpec, g)
                    if may_sentence :
                        # continue if and only if MayFormSentence is true
                        for nextNode in this_node.nextList:
                            if not nextNode.visited:
                                nextNode.visited = True
                                node_visited.put(nextNode.after.wordStr)
                    else :
                        # No way to form sentence, remove from the list and go back
                        # todo: managing sentence_so_far may need to be changed
                        sentence_so_far.remove(this_word)
    if highest_prob_sentence != []:
        sentence = " ".join(str(x) for x in highest_prob_sentence)
        print("\"" + sentence + "\" with probability " + str(prob))
        print("Total nodes onsidered: " + str(node_count))
    else :
        print("No valid sentence can be formed.")


##############################################################
generate("benjamin", p1struct, "input.txt")

