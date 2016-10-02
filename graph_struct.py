##################################################################
# Structure classes for graph.

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
        print("### " + self.word.wordStr + "-" + nextWord  +" prob: " + str(next_prob))
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
        # print("Sentence: " + sentenceStr)
        print("sentence_so_far(" + str(len(sentence)) + " words): [ " + sentenceStr + "]")
        return sentence

#################################################################

# for parent-child-dictionary structure

class ChildDict:
    def __init__(self, word):
        self.word = word
        self.parents = []

    def addParent(self, parent):
        self.parents.append(parent)

    def getUncheckedParent(self):
        for p in self.parents:
            if not p.checked:
                p.checkParent()
                return p.word.wordStr + "-" + p.word.type
        return ""



class ParentDict:
    def __init__(self,word):
        self.word = word
        self.checked = False

    def checkParent(self):
        self.checked = True
