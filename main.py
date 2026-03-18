test_truth_table = [
    [0, 0],
    [2, 0],
    ["X", "X"],
    [0, 4],
    ["X", "X"],
] #expl taken from auto5, to test while we cannot load from file

alpha_size = 2 #size of the alphabet, will be read from file
nb_states = 5 #number of states, will be read from file

def is_complete(auto):
    is_comp = True
    for row in (auto):
        if "X" in row:
            is_comp = False
            break
    return is_comp

def completion(auto):
    for i in range(nb_states):
        for j in range(alpha_size):
            if auto[i][j] == "X":
                auto[i][j] = -1 #-1 is sink state, on replace après
    sink_state = []
    for i in range(alpha_size):
        sink_state.append(-1)
    auto.append(sink_state)



print(test_truth_table)
print(is_complete(test_truth_table))
completion(test_truth_table)
print(test_truth_table)