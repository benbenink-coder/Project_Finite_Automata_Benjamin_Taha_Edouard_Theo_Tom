test_truth_table = [
    [0, 0],
    [2, 0],
    ["X", "X"],
    [0, 4],
    ["X", "X"],
] #expl taken frocdm auto5, to test while we cannot load from file

def read_txt(filename):
    with open(filename) as f:
        nbSymbols = f.readline()
        nbState = f.readline()
        print("Nb of symbols : " + nbSymbols)
        print("Nb of States : " + nbState)
        nbInitial = f.read(1)
        initialStates = f.readline().strip().split(" ")# We remove all spaces and \n and put it in the list
        nbFinal = f.read(1)
        finalStates = f.readline().strip().split(" ")
        print("{} Initial(s) state : {}".format(nbInitial, initialStates))  
        print("{} Final(s) state : {}".format(nbFinal, finalStates))  
        nbTransitions = f.read(1)
        print("Number of transitions : {}".format(nbTransitions))
        truthTable = [[[] for i in range(int(nbSymbols))] for j in range(int(nbState))]

        for x in f:
            stripped = x.strip()
            if stripped:  # Only process non-empty lines
                print(ord(x[1]))
                print(int(x[0]))
                truthTable[int(x[0])][ord(x[1])-97].append(int(x[2]))  #truthTable[nodeA][transitionNumber(a = 0, z=26)] = nodeB
        
        ## NB : The code below was written using Gen AI, as it is only visual and requires no logic

        print("\nTruth Table:")
        # Create header with column labels (a, b, c, ...)
        header = "State | " + " | ".join(f'{chr(97+j):>4}' for j in range(len(truthTable[0])))
        print(header)
        print("-" * len(header))
        for i, row in enumerate(truthTable):
            print(f"{i:>5} | {' | '.join(f'{str(val):>4}' for val in row)}")
        print("-" * len(header))


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
read_txt("test_automata/test_fa07.txt")