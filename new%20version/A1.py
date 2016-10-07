import sys
from queue import Queue
from decimal import Decimal

#########################################################
# stack structure
class Stack():
    def __init__(self):
        self.stack = []
        self.length = 0

    def push(self, item):
        if not self.stack:
            self.stack = [ item ]
        else:
            self.stack = [item ] + self.stack
        self.length += 1

    def pop(self):
        if not self.stack:
            return
        else:
            item = self.stack.pop(0)
            self.length -= 1
            return item

    def empty(self):
        isEmpty = False
        if not self.stack:
            isEmpty = True
        return isEmpty

##########################################################

class Word:

    def __init__(self, word_string_with_tag, probability=Decimal(1)):
        self.string = word_string_with_tag[0]
        self.part_of_speech = word_string_with_tag[1]
        self.probability = probability
        self.prev = None
        self.depth = 0

    def __eq__(self, other):
        return self.string == other.string and self.part_of_speech == other.part_of_speech

    def __str__(self):
        string = self.string + "/" + self.part_of_speech
        if self.probability != 1:
            string += "//" + str(self.probability)
        return string

    def __hash__(self):
        return hash((self.string, self.part_of_speech))

    def generate_sentence_word_list(self):
        sentence = [self]
        current_word = self
        while current_word.prev is not None:
            sentence = [current_word.prev] + sentence
            current_word = current_word.prev
        return sentence


def parse(file_name):

    try:
        file = open(file_name)
    except FileNotFoundError:
        print("Error: File \"" + file_name + "\" was not found!")
        sys.exit(1)

    graph = {}
    for line in file.readlines():
        pair_of_words = line.split('//')
        word = Word(pair_of_words[0].split('/'))
        probability = pair_of_words[2]
        neighbor_word = Word(pair_of_words[1].split('/'), Decimal(probability))

        if word not in graph:
            graph[word] = [neighbor_word]
        else:
            neighbor_words = graph[word]
            neighbor_words.append(neighbor_word)
            graph[word] = neighbor_words

    return graph


def calculate_probability_of_sentence(sentence):

    probability = Decimal(1)
    for word in sentence:
        probability *= word.probability
    return probability


def duplicate_word(word):
    new_word = Word([word.string, word.part_of_speech], word.probability)
    return new_word


def filter_list_of_words_by_tag(neighbor_words, part_of_speech):
    return [neighbor_word for neighbor_word in neighbor_words if neighbor_word.part_of_speech == part_of_speech]


def filter_list_of_words_by_max_probability(neighbor_words):
    if not neighbor_words:
        return neighbor_words
    max_probability = max(neighbor_word.probability for neighbor_word in neighbor_words)
    return [neighbor_word for neighbor_word in neighbor_words if neighbor_word.probability == max_probability]


def get_sentence_from_word_list(sentence):

    string = ""
    num_words = len(sentence)
    for i in range(num_words):
        string += sentence[i].string
        if i < num_words - 1:
            string += " "
    return string


###########################################################################
# A1Q3 - generate using DFS
def run_dfs(starting_word, sentence_spec, graph):
    num_words_considered = 0
    highest_probability = Decimal(0)
    highest_probability_sentence_word_list = []

    root_word = Word([starting_word, sentence_spec[0]])
    if root_word not in graph:
        print("Starting word \"" + starting_word + "\" was not found in the provided input file.")
        return

    sentence_spec_len = len(sentence_spec) - 1

    my_stack = Stack()
    my_stack.push(root_word)
    while not my_stack.empty():
        current_word = my_stack.pop()
        num_words_considered += 1

        if current_word.depth == sentence_spec_len:

            sentence_word_list = current_word.generate_sentence_word_list()
            current_sentence_probability = calculate_probability_of_sentence(sentence_word_list)

            if current_sentence_probability > highest_probability:

                highest_probability = current_sentence_probability
                highest_probability_sentence_word_list = sentence_word_list
        else:

            if current_word not in graph:
                continue

            neighbor_words = filter_list_of_words_by_tag(graph[current_word], sentence_spec[current_word.depth + 1])

            for neighbor in neighbor_words:
                duplicate = duplicate_word(neighbor)
                duplicate.prev = current_word
                duplicate.depth = current_word.depth + 1
                my_stack.push(duplicate)


    if highest_probability_sentence_word_list:
        sentence = get_sentence_from_word_list(highest_probability_sentence_word_list)
        print("\"" + sentence + "\" with probability " + str(highest_probability))
        print("Total nodes considered: " + str(num_words_considered))
    else:
        print("No valid sentence can be formed")


###########################################################################
# A1Q3 - generate using BFS
def run_bfs(starting_word, sentence_spec, search_strategy, graph):

    num_words_considered = 0
    highest_probability = Decimal(0)
    highest_probability_sentence_word_list = []

    root_word = Word([starting_word, sentence_spec[0]])
    if root_word not in graph:
        print("Starting word \"" + starting_word + "\" was not found in the provided input file.")
        return

    sentence_spec_len = len(sentence_spec) - 1

    my_queue = Queue()
    my_queue.put(root_word)

    while not my_queue.empty():

        current_word = my_queue.get()
        num_words_considered += 1

        if current_word.depth == sentence_spec_len:

            sentence_word_list = current_word.generate_sentence_word_list()
            current_sentence_probability = calculate_probability_of_sentence(sentence_word_list)

            if current_sentence_probability > highest_probability:

                highest_probability = current_sentence_probability
                highest_probability_sentence_word_list = sentence_word_list
        else:

            if current_word not in graph:
                continue

            neighbor_words = filter_list_of_words_by_tag(graph[current_word], sentence_spec[current_word.depth + 1])

            if search_strategy == HEURISTIC1 and current_word.depth + 1 == sentence_spec_len \
                    or search_strategy == HEURISTIC2:
                neighbor_words = filter_list_of_words_by_max_probability(neighbor_words)

            for neighbor in neighbor_words:
                duplicate = duplicate_word(neighbor)
                duplicate.prev = current_word
                duplicate.depth = current_word.depth + 1
                my_queue.put(duplicate)

    if highest_probability_sentence_word_list:
        sentence = get_sentence_from_word_list(highest_probability_sentence_word_list)
        print("\"" + sentence + "\" with probability " + str(highest_probability))
        print("Total nodes considered: " + str(num_words_considered))
    else:
        print("No valid sentence can be formed")


def generate(starting_word, sentence_spec, search_strategy, file_name):

    graph = parse(file_name)
    if search_strategy == DFS:
        run_dfs(starting_word, sentence_spec, graph)
    elif search_strategy == BFS or search_strategy == HEURISTIC1 or search_strategy == HEURISTIC2:
        run_bfs(starting_word, sentence_spec, search_strategy, graph)


###########################################################################
# A1Q1 - generate using BFS
def generate_bfs(starting_word, sentence_spec, file_name):
    graph = parse(file_name)
    num_words_considered = 0
    highest_probability = Decimal(0)
    highest_probability_sentence_word_list = []

    root_word = Word([starting_word, sentence_spec[0]])
    if root_word not in graph:
        print("Starting word \"" + starting_word + "\" was not found in the provided input file.")
        return

    sentence_spec_len = len(sentence_spec) - 1

    my_queue = Queue()
    my_queue.put(root_word)

    while not my_queue.empty():

        current_word = my_queue.get()
        num_words_considered += 1

        if current_word.depth == sentence_spec_len:

            sentence_word_list = current_word.generate_sentence_word_list()
            current_sentence_probability = calculate_probability_of_sentence(sentence_word_list)

            if current_sentence_probability > highest_probability:

                highest_probability = current_sentence_probability
                highest_probability_sentence_word_list = sentence_word_list
        else:

            if current_word not in graph:
                continue

            neighbor_words = filter_list_of_words_by_tag(graph[current_word], sentence_spec[current_word.depth + 1])

            for neighbor in neighbor_words:
                duplicate = duplicate_word(neighbor)
                duplicate.prev = current_word
                duplicate.depth = current_word.depth + 1
                my_queue.put(duplicate)

    if highest_probability_sentence_word_list:
        sentence = get_sentence_from_word_list(highest_probability_sentence_word_list)
        print("\"" + sentence + "\" with probability " + str(highest_probability))
        print("Total nodes considered: " + str(num_words_considered))
    else:
        print("No valid sentence can be formed")



FILE_NAME = "../input.txt"

BFS = "BREADTH_FIRST"
DFS = "DEPTH_FIRST"
HEURISTIC1 = "HEURISTIC1"
HEURISTIC2 = "HEURISTIC2"

STARTING_WORD = "hans"
SENTENCE_SPEC = ["NNP", "VBD", "DT", "NN"]

STARTING_WORD1 = "benjamin"
SENTENCE_SPEC1 = ["NNP", "VBD", "DT", "NN"]

STARTING_WORD2 = "a"
SENTENCE_SPEC2 = ["DT", "NN", "VBD", "NNP"]

STARTING_WORD3 = "benjamin"
SENTENCE_SPEC3 = ["NNP", "VBD", "DT", "JJS", "NN"]

STARTING_WORD4 = "a"
SENTENCE_SPEC4 = ["DT", "NN", "VBD", "NNP", "IN", "DT", "NN"]

MY_STARTING_WORD = "hans"
MY_SENTENCE_SPEC = ["NNP", "VBD"]


def run_test(search_strategy):

    print("=====RUN TEST FOR " + search_strategy + "======")
    print("EXAMPLE")
    generate(STARTING_WORD, SENTENCE_SPEC, search_strategy, FILE_NAME)

    print("TEST 1:")
    generate(STARTING_WORD1, SENTENCE_SPEC1, search_strategy, FILE_NAME)
    print("TEST 2:")
    generate(STARTING_WORD2, SENTENCE_SPEC2, search_strategy, FILE_NAME)
    print("TEST 3:")
    generate(STARTING_WORD3, SENTENCE_SPEC3, search_strategy, FILE_NAME)
    print("TEST 4:")
    generate(STARTING_WORD4, SENTENCE_SPEC4, search_strategy, FILE_NAME)

    print("=====END TEST FOR " + search_strategy + "=====\n")


def run_bfs_test():
    print("=====A1- BFS generate======")
    print("EXAMPLE")
    generate_bfs(STARTING_WORD, SENTENCE_SPEC, FILE_NAME)

    print("TEST 1:")
    generate_bfs(STARTING_WORD1, SENTENCE_SPEC1, FILE_NAME)
    print("TEST 2:")
    generate_bfs(STARTING_WORD2, SENTENCE_SPEC2, FILE_NAME)
    print("TEST 3:")
    generate_bfs(STARTING_WORD3, SENTENCE_SPEC3, FILE_NAME)
    print("TEST 4:")
    generate_bfs(STARTING_WORD4, SENTENCE_SPEC4, FILE_NAME)

    print("========END A1 TEST=====\n")

run_test(BFS)
run_bfs_test()
run_test(DFS)
# run_test(DFS)
#run_test(HEURISTIC1)
#run_test(HEURISTIC2)
