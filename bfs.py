import queue
import decimal
import graph_struct
import common


# main function that generates sentence using BFS
def generate(startingWord, sentenceSpec, graph):
    sentence_so_far = []
    highest_prob_sentence = []
    prob = decimal.Decimal(0)

    # parse graph from given file
    g = graph_struct.parseGraph(graph)
    # print("# of items in Graph: " + str(len(g)))
    # graph_struct.printGraph(g)

    # validate the first word
    initGraphKey = startingWord + "-" + sentenceSpec[0]
    if not initGraphKey in g :
        # init word is not valid - return
        print("No valid sentence can be formed")
        return

    # init word is valid - continue
    # print(initGraphKey + " is valid!")

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
            node_count += 1

            # print("this_word : " + this_key + ", parents: " +  ">".join(str(y) for y in this_queue.parents))

            sentence_so_far = this_queue.generateSentence()
            is_sentence = common.isValidSentence(sentence_so_far, sentenceSpec)

            if is_sentence:
                # update the sentence that has highest probability
                this_prob = common.calculateProb(sentence_so_far, g)
                # print("this_prob: " + str(this_prob))

                if this_prob > prob:
                    prob = this_prob
                    highest_prob_sentence = sentence_so_far
            else :
                may_sentence = common.mayFormValidSentence(sentence_so_far, sentenceSpec)
                if may_sentence:
                    # continue if and only if MayFormSentence is true

                    for nextNode in this_node.nextList:
                        if not nextNode.visited:
                            # nextNode.visited = True
                            pc_key = nextNode.after.wordStr + "-" + nextNode.after.type

                            next_parent = [this_key]
                            if this_queue.parents:
                                next_parent = this_queue.parents + next_parent
                            next_queue_entry = graph_struct.QueueEntry(pc_key, next_parent)
                            node_visited.put(next_queue_entry)

    if highest_prob_sentence != []:
        # sentence = " ".join(str(x) for x in highest_prob_sentence)
        sentence = common.makeString(highest_prob_sentence)

        print("\"" + sentence + "\" with probability " + str(prob))
        print("Total nodes considered: " + str(node_count))
    else:
        print("No valid sentence can be formed")

