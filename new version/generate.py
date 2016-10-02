import sys
import queue

STARTING_WORD = "hans"
SENTENCE_SPEC = ["NNP", "VBD", "DT", "NN"]
FILE_NAME = "../input.txt"


class Word:

    def __init__(self, word_string_with_tag):
        self.string = word_string_with_tag[0]
        self.part_of_speech = word_string_with_tag[1]

    def __eq__(self, other):
        return self.string == other.string and self.part_of_speech == other.part_of_speech

    def __str__(self):
        return self.string + "/" + self.part_of_speech

    def __hash__(self):
        return hash((self.string, self.part_of_speech))


class NeighborWord(Word):

    def __init__(self, word_string_with_tag, probability):
        super().__init__(word_string_with_tag)
        self.probability = probability
        self.visited = False
        self.prev = None

    def __str__(self):
        return super().__str__() + "//" + self.probability


# def add_word_to_sequence(sequence, word, part_of_speech, probability):
#
# def duplicate_sequence(sequence):
#
# def is_valid_sentence(sequence):
#
# def may_form_valid_sentence(sequence):

def parse(file_name):

    try:
        file = open(file_name)
    except FileNotFoundError:
        print("Error: File \"" + file_name + "\" was not found!" )
        sys.exit(1)

    graph = {}
    for line in file.readlines():
        pair_of_words = line.split('//')
        word = Word(pair_of_words[0].split('/'))
        probability = pair_of_words[2]
        neighbor_word = NeighborWord(pair_of_words[1].split('/'), probability)

        if word not in graph:
            graph[word] = [neighbor_word]
        else:
            neighbor_words = graph[word]
            neighbor_words.append(neighbor_word)
            graph[word] = neighbor_words

    return graph


def print_graph(graph):

    for word in graph:
        print("\nWord: ", end="")
        print(word)
        print("\nNeighbors: ")
        for neighbor_word in graph[word]:
            print(neighbor_word)


def run_bfs(starting_word, sentence_spec, graph):

    my_queue = queue.Queue()
    current_level_of_tree = 0

    prev = {}
    visited = {}

    root_word = Word([starting_word, sentence_spec[current_level_of_tree]])
    my_queue.put(root_word)

    while my_queue.not_empty:

        current_word = my_queue.get()
        if my_queue.empty():
            current_level_of_tree += 1

        if current_word not in graph:
            continue

        neighbor_words = graph[current_word]
        filtered_neighbor_words = \
            filter(lambda neighbor_word: neighbor_word.part_of_speech == sentence_spec[current_level_of_tree],
                   neighbor_words)

        for neighbor in filtered_neighbor_words:
            if neighbor not in visited:
                # neighbor.visited = True
                visited[neighbor] = True
                prev[neighbor] = current_word
                # neighbor.prev = current_word
                my_queue.put(neighbor)


def generate(starting_word, sentence_spec, file_name):

    graph = parse(file_name)
    print_graph(graph)

    # run_bfs(starting_word, sentence_spec, graph)


generate(STARTING_WORD, SENTENCE_SPEC, FILE_NAME)
