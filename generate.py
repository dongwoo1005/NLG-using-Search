# example string from input (for test): there/EX//was/VBD//0.21311475409836064
# for A1P1, valid sentence structure is: "NNP", "VBD", "DT", "NN"
import queue
import decimal
import graph_struct

################################################################3
# global variables
p1struct = ["NNP", "VBD", "DT", "NN"]


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
        prob = decimal.Decimal(wlist[2])

        # generate word
        word1 = graph_struct.Word(word1list[0], word1list[1])
        word2 = graph_struct.Word(word2list[0], word2list[1])

        afternode = graph_struct.NextNode(word2, prob)

        if word1.wordStr in graph:
            thisnode = graph[word1.wordStr]
            thisnode.addNext(afternode)
            graph[word1.wordStr] = thisnode
        else:
            thisnode = graph_struct.GraphNode(word1)
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
            afterstring = afterstring + "(" + nextNode.after.wordStr + "[" + nextNode.after.type + "] ," + str(nextNode.prob) + ")"
            afterstring += ", "
        afterstring += "}"
        toprint = toprint + " - " + afterstring
        print(toprint)


############################################################
############################################################
# calculate probability of given sentence s
def calculateProb(s, graph) :
    sentence_len = len(s)
    init_word = s[0]
    prob = decimal.Decimal(1)
    for i in range(0, sentence_len):
        dest_word = s[i]
        this_prob = 1
        if init_word == dest_word:
            this_prob = 1
        else:
            origin = graph[init_word]
            this_prob = origin.probNext(dest_word)
        prob = prob * this_prob
        init_word = s[i]
    return prob


def trackSentencesSoFar(lastWord, initWord,  cp_dict) :
    sentence_so_far = []
    sentence_so_far.append(lastWord)
    if not cp_dict:
        return sentence_so_far
    else :
        # check and add to sentence so far until parent reach to initWord
        x = lastWord
        while x in cp_dict:
            parent = cp_dict[x]
            sentence_so_far = [parent] + sentence_so_far
            if parent == initWord:
                break
            else :
                x = parent
        sentenceStr = " ".join(str(y) for y in sentence_so_far)
        print("sentence_so_far: [ " + sentenceStr + " ]")
        return sentence_so_far




############################################################
############################################################
# main function that generates sentence using BFS
def generate(startingWord, sentenceSpec, graph):
    sentence_so_far = []
    highest_prob_sentence = []
    prob = decimal.Decimal(0)

    parent_child_dict = dict()  # dictionary to store the parent of given child

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
            #sentence_so_far.append(this_word)
            this_node = g[this_word]
            node_count += 1

            print("this_word : " + this_word)

            sentence_so_far = trackSentencesSoFar(this_word, startingWord, parent_child_dict)
            is_sentence = isValidSentence(sentence_so_far, sentenceSpec, g)
            #if __name__ == '__main__':
            if is_sentence:
                # update the sentence that has highest probability
                this_prob = calculateProb(sentence_so_far, g)
                print("this_prob: " + str(this_prob))

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
                            parent_child_dict[nextNode.after.wordStr] = this_word
                            node_visited.put(nextNode.after.wordStr)

    if highest_prob_sentence != []:
        sentence = " ".join(str(x) for x in highest_prob_sentence)
        print("\"" + sentence + "\" with probability " + str(prob))
        print("Total nodes onsidered: " + str(node_count))
    else :
        print("No valid sentence can be formed.")


##############################################################
generate("benjamin", p1struct, "input.txt")

