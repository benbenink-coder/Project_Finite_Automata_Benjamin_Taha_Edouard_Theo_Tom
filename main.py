import os
import time


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
       
                if x[1] == "*":
                    truthTable[int(x[0])][-1].append(int(x[2]))
                else:   
  
                  truthTable[int(x[0])][ord(x[1])-97].append(int(x[2]))  #truthTable[nodeA][transitionNumber(a = 0, z=26)] = nodeB
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

def is_standard(truthTable, initialStates):
    if len(initialStates) >1:
        return False
    for state in truthTable:
        for word in state:
            for target in word:
                if target == initialStates[0]:
                    return False
    return True

def standardization(truthTable, initialStates):
    initial = [[] for i in range(len(truthTable[0]))]
    for i_state in initialStates:
        for i in range(len(truthTable[int(i_state)])):
            for j in range(len(truthTable[int(i_state)][i])):
                initial[i].append(truthTable[int(i_state)][i][j])
    truthTable.append(initial)
    initialStates = str(len(truthTable)-1)
    return truthTable, initialStates

def standardization_on_demand(truthTable, initialStates):
    if not is_standard(truthTable, initialStates):
        print("Do you want to standardize? Type 'yes' or 'no':")
        if input().lower() == "yes":
            truthTable, initialStates = standardization(truthTable, initialStates)
            printTruthTable(truthTable)
            return truthTable, initialStates
        else:
            return truthTable, initialStates
    print("The automata is already standardized!")
    return truthTable, initialStates

# COMPLETION PART

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
                truthTable[i][j] = [nbState]
    sink_state = [[nbState] for i in range(nbSymbols)]
    truthTable.append(sink_state)
    print("Sucessfully completed FA !")

# DETERMINIZATION PART

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
    print("* Deterministic : " + str(is_det))
    return is_det

def sls(arr):
    return sorted(list(set(arr)))

def determinize(nbSymbols, nbState, initialStates, finalStates, truthTable):
    newTruthTable = []
    toDo = []
    fakeStatesToIndices = {}

    newInitialStates = []
    newFinalStates = []
    
    toDo.append(sls(initialStates))

    indice = 0
    while (len(toDo)) > 0:
        stateName, stateRow = merge_states(toDo[0], truthTable, nbSymbols, toDo, fakeStatesToIndices, initialStates, finalStates, newInitialStates, newFinalStates)
        newTruthTable.append(stateRow)
        fakeStatesToIndices[stateName] = indice
        del toDo[0]
        indice +=1
    print(newInitialStates)
    print(newFinalStates)
    print(fakeStatesToIndices)
    printTruthTable(newTruthTable)


def merge_states(statesToMerge, truthTable, nbSymbols, toDo, fakeStatesToIndices, initialStates, finalStates, newInitialStates, newFinalStates):
    stateName = "".join(str(s) for s in statesToMerge)
    if (all(str(e) in initialStates for e in statesToMerge)):
        print("initial")
        newInitialStates.append(stateName)

    if (any(str(e) in finalStates for e in statesToMerge)):
        print("final")
        newFinalStates.append(stateName)

    stateRow = [[] for i in range(int(nbSymbols))]
    for i in range(int(nbSymbols)):
        trans = [] 
        for j in statesToMerge:
            trans.extend(truthTable[int(j)][i])
        trans = sls(trans) #remove duplicates and sort it asc so [2,1,3] and [3,2,1] etc.. are considered same
        stateRow[i] = "".join(str(s) for s in trans)
        if trans not in toDo and stateRow[i] not in fakeStatesToIndices.keys():
            toDo.append(trans)
    return stateName, stateRow


#MINIMIZATION PART
def normalize_truthTable_for_cdfa(truthTable):
    # Convert temporary sink (-1) into real sink index and enforce determinism
    normalizedTruthTable = []
    sinkIndex = len(truthTable) - 1

    for row in truthTable:
        newRow = []
        for trans in row:
            if len(trans) == 0:
                raise ValueError("Minimization requires a complete automaton.")
            if len(trans) > 1:
                raise ValueError("Minimization requires a deterministic automaton.")

            target = trans[0]
            if target == -1:
                target = sinkIndex

            newRow.append([target])
        normalizedTruthTable.append(newRow)

    return normalizedTruthTable


def reachable_states(initialStates, truthTable):
    # Classic DFS to keep only useful states
    if len(initialStates) != 1:
        raise ValueError("Minimization requires one initial state.")

    start = int(initialStates[0])
    visited = set([start])
    stack = [start]

    while stack:
        current = stack.pop()

        for trans in truthTable[current]:
            nxt = trans[0]
            if nxt not in visited:
                visited.add(nxt)
                stack.append(nxt)

    return sorted(list(visited))


def keep_only_reachable_states(nbSymbols, initialStates, finalStates, truthTable, stateNames):
    # Remove unreachable states before minimization
    truthTable = normalize_truthTable_for_cdfa(truthTable)
    reachable = reachable_states(initialStates, truthTable)

    oldToNew = {old: new for new, old in enumerate(reachable)}

    newTruthTable = []
    for oldState in reachable:
        newRow = []
        for s in range(nbSymbols):
            newRow.append([oldToNew[truthTable[oldState][s][0]]])
        newTruthTable.append(newRow)

    newInitialStates = [str(oldToNew[int(initialStates[0])])]

    newFinalStates = []
    for f in finalStates:
        f = int(f)
        if f in oldToNew:
            newFinalStates.append(str(oldToNew[f]))

    newStateNames = [stateNames[s] for s in reachable]

    return len(reachable), newInitialStates, newFinalStates, newTruthTable, newStateNames


def state_to_group(partition):
    # Map each state to its group index
    return {state: i for i, group in enumerate(partition) for state in group}


def display_partition(partition, stateNames, k):
    print(f"\nPartition P{k} :")
    for i, group in enumerate(partition):
        print(f"  G{i} = {{{', '.join(stateNames[s] for s in group)}}}")


def display_group_transitions(partition, nbSymbols, truthTable, stateNames, k):
    # Show transitions between groups instead of states
    print(f"Transitions between groups for P{k} :")
    groups = state_to_group(partition)

    for i, group in enumerate(partition):
        rep = group[0]  # representative
        transitions = []

        for s in range(nbSymbols):
            target = truthTable[rep][s][0]
            transitions.append(f"{chr(97+s)} -> G{groups[target]}")

        print(f"  G{i} ({', '.join(stateNames[s] for s in group)}) : {' ; '.join(transitions)}")


def refine_partition(partition, nbSymbols, truthTable):
    # Split groups based on transition signatures
    groups = state_to_group(partition)
    newPartition = []
    changed = False

    for group in partition:
        buckets = {}

        for state in group:
            signature = tuple(groups[truthTable[state][s][0]] for s in range(nbSymbols))
            buckets.setdefault(signature, []).append(state)

        split = list(buckets.values())
        newPartition.extend(split)

        if len(split) > 1:
            changed = True

    return newPartition, changed


def minimization(nbSymbols, nbState, initialStates, finalStates, truthTable, stateNames=None):
    # Default naming if none provided
    if stateNames is None:
        stateNames = [str(i) for i in range(nbState)]

    # Remove unreachable states first
    nbState, initialStates, finalStates, truthTable, stateNames = keep_only_reachable_states(
        nbSymbols, initialStates, finalStates, truthTable, stateNames
    )

    finalSet = set(int(f) for f in finalStates)

    # Initial partition: non-final vs final
    nonFinal = [s for s in range(nbState) if s not in finalSet]
    final = [s for s in range(nbState) if s in finalSet]

    partition = []
    if nonFinal:
        partition.append(nonFinal)
    if final:
        partition.append(final)

    k = 0
    display_partition(partition, stateNames, k)
    display_group_transitions(partition, nbSymbols, truthTable, stateNames, k)

    # Refinement loop
    while True:
        newPartition, changed = refine_partition(partition, nbSymbols, truthTable)
        if not changed:
            break

        partition = newPartition
        k += 1

        display_partition(partition, stateNames, k)
        display_group_transitions(partition, nbSymbols, truthTable, stateNames, k)

    groups = state_to_group(partition)

    # Build minimized automaton
    minimalTruthTable = []
    for group in partition:
        rep = group[0]
        newRow = []

        for s in range(nbSymbols):
            target = truthTable[rep][s][0]
            newRow.append([groups[target]])

        minimalTruthTable.append(newRow)

    minimalInitialStates = [str(groups[int(initialStates[0])])]

    minimalFinalStates = []
    for i, group in enumerate(partition):
        if any(s in finalSet for s in group):
            minimalFinalStates.append(str(i))

    # Keep track of which states were merged
    minimalStateContents = [[stateNames[s] for s in group] for group in partition]

    # Check if already minimal
    if len(partition) == nbState:
        print("\nThis CDFA was already minimal.")
    else:
        print("\nThis CDFA was not minimal.")

    print(f"Number of states before minimization : {nbState}")
    print(f"Number of states after minimization : {len(partition)}")

    return nbSymbols, len(partition), minimalInitialStates, minimalFinalStates, minimalTruthTable, minimalStateContents


def display_minimal_automaton(MCDFA):
    nbSymbols, nbState, initialStates, finalStates, truthTable, contents = MCDFA

    print("\n===== Minimal automaton (MCDFA) =====")
    print("Nb of symbols :", nbSymbols)
    print("Nb of States :", nbState)
    print(f"{len(initialStates)} Initial(s) state :", initialStates)
    print(f"{len(finalStates)} Final(s) state :", finalStates)

    # Required mapping table (important for grading)
    print("\nState correspondence:")
    for i, group in enumerate(contents):
        print(f"  {i} -> {{{', '.join(group)}}}")

    printTruthTable(truthTable)

# nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/test_fa05.txt")
# printTruthTable(truthTable)
# truthTable, initialStates = standardization_on_demand(truthTable,initialStates)
# print(initialStates)

# nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/test_fa07.txt")
# printTruthTable(truthTable)
# truthTable, initialStates = standardization_on_demand(truthTable,initialStates)

# print("*************************")
# anbSymbols = 2
# anbState = 5
# ainitialStates = [0]
# afinalStates = [4]
# atruthTable = [
#     [[0,1], [0]],
#     [[], [2]],
#     [[3], []],
#     [[4], []],
#     [[], []],
# ]
# determinize(anbSymbols, anbState, ainitialStates, afinalStates, atruthTable)
# print("*************************")

# is_complete(truthTable)
# completion(nbSymbols, nbState, truthTable)
# is_complete(truthTable)
# printTruthTable(truthTable)


# if is_deterministic(initialStates, truthTable):
#     MCDFA = minimization(nbSymbols, len(truthTable), initialStates, finalStates, truthTable)
#     display_minimal_automaton(MCDFA)
# else:
#     print("Cannot minimize: automaton is not deterministic.")



def recognize_word(word, nbSymbols, nbState, initialStates, finalStates, truthTable):
#i removed the automaton reading to pass it as parameter, saving memory and being more efficient

    # Store all possible current states
    # This is needed because the automaton can be non-deterministic
    current_states = []
    for state in initialStates:
        current_states.append(int(state))

    # Read the word letter by letter after it has been fully typed
    for letter in word:
        # Convert the letter into the corresponding column index
        # a -> 0, b -> 1, c -> 2, ...
        column = ord(letter) - 97

        # If the letter is outside the alphabet, reject the word
        if column < 0 or column >= nbSymbols:
            return False

        # This list will contain all states reachable after reading the letter
        next_states = []

        # For each current possible state
        for state in current_states:
            # Add all reachable destination states for this letter
            for dest in truthTable[state][column]:
                if dest not in next_states:
                    next_states.append(dest)

        # If no transition is possible, reject the word
        if len(next_states) == 0:
            return False

        # Update the current possible states
        current_states = next_states

    # After reading the whole word, accept if at least one current state is final
    for state in current_states:
        if str(state) in finalStates:
            return True

    # Otherwise reject
    return False


def read_word(nbSymbols, nbState, initialStates, finalStates, truthTable):
    # Ask the user to type a full word
    word = input("Type a word to test (or 'end' to stop): ")

    # Repeat until the user types "end"
    while word != "end":
        # Test if the automaton recognizes the word
        if recognize_word(word, nbSymbols, nbState, initialStates, finalStates, truthTable):
            print("Yes")
        else:
            print("No")

        # Ask for another word
        word = input("Type a word to test (or 'end' to stop): ")


def menu():
    print("Welcome to our Finite Automata Software. (press ctrl+c to quit)")
    time.sleep(1)
    automataList = os.listdir("test_automata")
    automataList.sort()
    while True:
        print("Below is the list of all automatas in the 'test_automata' directory" )
        for i in range(len(automataList)):
            print("{}.".format(i+1), automataList[i])
            time.sleep(0.01)
        choice = int(input("Input your choice (n° of the automata)\n\n"))
        print("You selected automaton : {}".format(automataList[choice-1]))
        nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/"+automataList[choice-1])
        print("Below is the truth table of automaton {}".format(automataList[choice-1]))
        printTruthTable(truthTable, initialStates, finalStates)
        while True:
            print("Here are the operation you can apply on the automaton : \n 1. Standardize \n 2. Determinize \n 3. Complete \n 4. Minimize \n 5. Read Word")
            opChoice = int(input("Give the operation number you want to apply : "))
            match opChoice:
                case 1:
                    standardization(truthTable, initialStates)
                case 2: 
                    determinize(nbSymbols, nbState, initialStates, finalStates, truthTable)
                case 3:
                    completion(nbSymbols, nbState, truthTable)
                case 4:
                    minimization(nbSymbols, nbState, initialStates, finalStates, truthTable)
                case 5:
                    read_word(nbSymbols, nbState, initialStates, finalStates, truthTable)

menu()
read_word("test_automata/test_fa07.txt")