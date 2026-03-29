import re
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
        nbTransitions = f.readline() 
        print("Number of transitions : {}".format(nbTransitions))
        truthTable = [[[] for i in range(int(nbSymbols)+1)] for j in range(int(nbState))] ##last column is always *
        for x in f:
            print(x)
            stripped = x.strip()
            if stripped:  # Only process non-empty lines
                match = re.search(r"(\d+)([\*a-z])(\d+)", x) #This uses regular expressions to read the strings of transitions (as we could have 111111*222222 and we would still want our programm to work)
                if match:
                    first_num = match.group(1)
                    separator = match.group(2)
                    second_num = match.group(3)
                if separator == "*":
                    truthTable[int(first_num)][-1].append(int(second_num))
                else:
                    print(x[0], x[1], x[2])
                    truthTable[int(first_num)][ord(separator)-97].append(int(second_num))  #truthTable[nodeA][transitionNumber(a = 0, z=26)] = nodeB
        return int(nbSymbols), int(nbState), initialStates, finalStates, truthTable
    
def printTruthTable(truthTable, initialStates, finalStates):
    ## NB : The code below was written using Gen AI, as it is only visual and requires no logic
    print("\nTruth Table:")
    # Create header with column labels (a, b, c, ..., *)
    header = "    | State | " + " | ".join(f'{chr(97+j):>4}' for j in range(len(truthTable[0])-1)) + " | " + f"{'*':>4}"
    print(header)
    print("-" * len(header))
    for i, row in enumerate(truthTable):
        # Determine markers for initial and final states
        marker = ""
        if str(i) in initialStates:
            marker += "->"
        else:
            marker += "  "
        if str(i) in finalStates:
            marker += "<-"
        else:
            marker += "  "
        
        print(f"{marker} | {i:>5} | {' | '.join(f'{str(val):>4}' for val in row)}")
    print("-" * len(header))

