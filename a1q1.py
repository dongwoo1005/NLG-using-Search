import queue
import decimal
import graph_struct

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

        graphKey = word1.wordStr + "-" + word1.type

        if graphKey in graph:
            thisnode = graph[graphKey]
            thisnode.addNext(afternode)
            graph[graphKey] = thisnode
        else:
            thisnode = graph_struct.GraphNode(word1)
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

############################################################
############################################################
def trackSentencesSoFar(this_key, init_key, pc_dict):
    sentence_so_far = []
    sentence_so_far.append(this_key)

    if this_key == init_key :
        return [this_key]

    if not pc_dict:
        return sentence_so_far
    else:
        # check and add to sentence so far until parent reach to initKey
        x = this_key
        while x in pc_dict:
            this_child = pc_dict[x]
            parent = this_child.getUncheckedParent()
            sentence_so_far = [parent] + sentence_so_far
            if parent == init_key:
                break
            else:
                x = parent
        sentenceStr = " ".join(str(y) for y in sentence_so_far)
        print("sentence_so_far(" + str(len(sentence_so_far)) + " words): [ " + sentenceStr + "]")
        return sentence_so_far

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

    # validate the first word
    initGraphKey = startingWord + "-" + sentenceSpec[0]
    if not initGraphKey in g :
        # init word is not valid - return
        print("No valid sentence can be formed")
        return

    # init word is valid - continue
    print(initGraphKey + " is valid!")

    # do BFS
    node_visited = queue.Queue()
    node_count = 0

    initQueueEntry = graph_struct.QueueEntry(initGraphKey, [])

    node_visited.put(initQueueEntry)

    while not node_visited.empty():
        this_queue = node_visited.get()
        this_key = this_queue.wordKey
        if this_key in g:
            this_node = g[this_key]
            this_type = this_node.word.type
            node_count += 1

            print("this_word : " + this_key + ", parents: " +  ">".join(str(y) for y in this_queue.parents))

            # sentence_so_far = trackSentencesSoFar(this_key, initGraphKey, parent_child_dict)
            sentence_so_far = this_queue.generateSentence()
            is_sentence = isValidSentence(sentence_so_far, sentenceSpec)

            if is_sentence:
                # update the sentence that has highest probability
                this_prob = calculateProb(sentence_so_far, g)
                print("this_prob: " + str(this_prob))

                if this_prob > prob:
                    prob = this_prob
                    highest_prob_sentence = sentence_so_far
            else :
                may_sentence = mayFormValidSentence(sentence_so_far, sentenceSpec)
                if may_sentence:
                    # continue if and only if MayFormSentence is true

                    # make parent structure
                    parent_val = graph_struct.ParentDict(this_node.word)

                    for nextNode in this_node.nextList:
                        if not nextNode.visited:
                            # nextNode.visited = True
                            pc_key = nextNode.after.wordStr + "-" + nextNode.after.type

                            # if pc_key in parent_child_dict:
                            #    this_child = parent_child_dict[pc_key]
                            #    this_child.addParent(parent_val)
                            #    parent_child_dict[pc_key] = this_child
                            #else :
                            #    this_child = graph_struct.ChildDict(nextNode.after)
                            #    this_child.addParent(parent_val)
                            #    parent_child_dict[pc_key] = this_child

                            # pc_val = this_key
                            # parent_child_dict[pc_key] = pc_val
                            next_parent = [this_key]
                            if this_queue.parents:
                                next_parent = this_queue.parents + next_parent
                            # next_parent = this_queue.parents.append(this_key)
                            next_queue_entry = graph_struct.QueueEntry(pc_key, next_parent)
                            node_visited.put(next_queue_entry)

    if highest_prob_sentence != []:
        # sentence = " ".join(str(x) for x in highest_prob_sentence)
        sentence = makeString(highest_prob_sentence)

        print("\"" + sentence + "\" with probability " + str(prob))
        print("Total nodes considered: " + str(node_count))
    else:
        print("No valid sentence can be formed")




############################################################################
############################################################################
p1struct = ["NNP", "VBD", "DT", "NN"]

generate("hans", p1struct, "input.txt")