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
        return nbSymbols, nbState, initialStates, finalStates, truthTable
    
def printTruthTable(truthTable):
        ## NB : The code below was written using Gen AI, as it is only visual and requires no logic
        print("\nTruth Table:")
        # Create header with column labels (a, b, c, ...)
        header = "State | " + " | ".join(f'{chr(97+j):>4}' for j in range(len(truthTable[0])))
        print(header)
        print("-" * len(header))
        for i, row in enumerate(truthTable):
            print(f"{i:>5} | {' | '.join(f'{str(val):>4}' for val in row)}")
        print("-" * len(header))

def is_complete(truthTable):
    is_comp = True
    for row in (truthTable):
        if "-" in row:
            is_comp = False
            break
    return is_comp

def completion(nbSymbols, nbState, truthTable):
    for i in range(nbState):
        for j in range(nbSymbols):
            if truthTable[i][j] == "-":
                truthTable[i][j] = -1 #-1 is sink state, on replace après
    sink_state = [-1 for i in range(nbSymbols)]
    truthTable.append(sink_state)


def is_deterministic(nbSymbols, nbState, initialStates, truthTable):
    if len(initialStates) > 1:
        return False
    




nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/test_fa07.txt")
print(is_complete(truthTable))
completion(nbSymbols, nbState, truthTable)
print(is_complete(truthTable))
print(truthTable)