import sys
from queue import Queue
from decimal import Decimal


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

    def generate_sentence(self):
        sentence = [self]
        current_word = self
        while current_word.prev is not None:
            sentence = [current_word.prev] + sentence
            current_word = current_word.prev
        return sentence

    def get_probability_of_sentence(self):
        probability = self.probability
        current_word = self
        while current_word.prev is not None:
            probability *= current_word.probability
            current_word = current_word.prev
        return probability


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


def print_graph(graph):

    print("=========PRINT_GRAPH============")
    for word in graph:
        print("\nWord: ", end="")
        print(word)
        print("Neighbors: ")
        for neighbor_word in graph[word]:
            print(neighbor_word)
    print("========END_PRINT_GRAPH=========")


def is_sentence_valid(sentence, sentence_spec):

    if len(sentence) != len(sentence_spec):
        return False

    for i in range(len(sentence)):
        if sentence[i].part_of_speech != sentence_spec[i]:
            return False

    return True


def calculate_probability_of(sentence):

    probability = Decimal(1)
    for word in sentence:
        probability *= word.probability
    return probability


def build_sentence(sentence):

    string = ""
    num_words = len(sentence)
    for i in range(num_words):
        string += sentence[i].string
        if i < num_words - 1:
            string += " "
    return string


def duplicate_word(word):
    new_word = Word([word.string, word.part_of_speech], word.probability)
    return new_word


def run_bfs(starting_word, sentence_spec, graph):

    num_words_considered = 0
    highest_probability = Decimal(0)
    highest_probability_sentence = []

    root_word = Word([starting_word, sentence_spec[0]])
    if root_word not in graph:
        print("Starting word \"" + starting_word + "\" was not found in the provided input file.")
        return

    my_queue = Queue()
    my_queue.put(root_word)

    while not my_queue.empty():

        current_word = my_queue.get()
        num_words_considered += 1

        current_sentence = current_word.generate_sentence()

        if is_sentence_valid(current_sentence, sentence_spec):

            current_sentence_probability = calculate_probability_of(current_sentence)
            if current_sentence_probability > highest_probability:

                highest_probability = current_sentence_probability
                highest_probability_sentence = current_sentence
        else:
            if current_word not in graph:
                continue
            neighbor_words = graph[current_word]

            filtered_neighbor_words = \
                [neighbor_word for neighbor_word in neighbor_words
                 if neighbor_word.part_of_speech == sentence_spec[current_word.depth + 1]]

            if current_word.depth + 1 == len(sentence_spec) - 1 and filtered_neighbor_words:
                max_probability = max(neighbor_word.probability for neighbor_word in filtered_neighbor_words)
                filtered_neighbor_words = \
                    [neighbor_word for neighbor_word in filtered_neighbor_words
                     if neighbor_word.probability == max_probability]

            for neighbor in filtered_neighbor_words:
                duplicate = duplicate_word(neighbor)
                duplicate.prev = current_word
                duplicate.depth = current_word.depth + 1
                my_queue.put(duplicate)

    if highest_probability_sentence:
        sentence = build_sentence(highest_probability_sentence)
        print("\"" + sentence + "\" with probability " + str(highest_probability))
        print("Total nodes considered: " + str(num_words_considered))
    else:
        print("No valid sentence can be formed")


def generate(starting_word, sentence_spec, file_name):

    graph = parse(file_name)
    # print_graph(graph)
    run_bfs(starting_word, sentence_spec, graph)


FILE_NAME = "../input.txt"

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

print("EXAMPLE")
generate(STARTING_WORD, SENTENCE_SPEC, FILE_NAME)

print("TEST 1:")
generate(STARTING_WORD1, SENTENCE_SPEC1, FILE_NAME)
print("TEST 2:")
generate(STARTING_WORD2, SENTENCE_SPEC2, FILE_NAME)
print("TEST 3:")
generate(STARTING_WORD3, SENTENCE_SPEC3, FILE_NAME)
print("TEST 4:")
generate(STARTING_WORD4, SENTENCE_SPEC4, FILE_NAME)
