# test file for search functions
import bfs
import dfs
# inputs
graphFileName = "input.txt"
startingWord1 = "benjamin"
startingWord2 = "a"
sentenceSpec1 = ["NNP", "VBD", "DT", "NN"]
sentenceSpec2 = [ "DT", "NN", "VBD", "NNP"]
sentenceSpec3 = [ "NNP", "VBD", "DT", "JJS", "NN"]
sentenceSpec4 = [ "DT", "NN", "VBD", "NNP", "IN", "DT", "NN" ]

# 1. BFS Test
print("------ Part 2 BFS------")
print("Test 1:")
bfs.generate(startingWord1, sentenceSpec1, graphFileName)
print("Test 2:")
bfs.generate(startingWord2, sentenceSpec2, graphFileName)
print("Test 3:")
bfs.generate(startingWord1, sentenceSpec3, graphFileName)
print("Test 4:")
bfs.generate(startingWord2, sentenceSpec4, graphFileName)

print("\n")

print("------ Part 2 DFS------")
print("Test 1:")
dfs.generate_DFS(startingWord1, sentenceSpec1, graphFileName)
print("Test 2:")
dfs.generate_DFS(startingWord2, sentenceSpec2, graphFileName)
print("Test 3:")
dfs.generate_DFS(startingWord1, sentenceSpec3, graphFileName)
print("Test 4:")
dfs.generate_DFS(startingWord2, sentenceSpec4, graphFileName)