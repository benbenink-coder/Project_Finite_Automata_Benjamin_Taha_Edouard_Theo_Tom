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
        return int(nbSymbols), int(nbState), initialStates, finalStates, truthTable
    
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
        for trans in row:
            if len(trans) == 0:
                is_comp = False
                break
    print("* Complete : " + str(is_comp))
    return is_comp

def completion(nbSymbols, nbState, truthTable):
    for i in range(nbState):
        for j in range(nbSymbols):
            if len(truthTable[i][j]) == 0:
                truthTable[i][j] = [-1] #-1 is sink state, on replace après
    sink_state = [[-1] for i in range(nbSymbols)]
    truthTable.append(sink_state)
    print("Sucessfully completed FA !")

def is_deterministic(initialStates, truthTable):
    is_det = True
    if len(initialStates) > 1:
        is_det = False
    else:   
        for row in (truthTable):
            for trans in row:
                if len(trans) > 1:
                    is_det = False
                    break
    print("* Determinstic : " + str(is_det))
    return is_det


nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/test_fa07.txt")
printTruthTable(truthTable)

is_complete(truthTable)
completion(nbSymbols, nbState, truthTable)
is_complete(truthTable)
printTruthTable(truthTable)

is_deterministic(initialStates, truthTable)