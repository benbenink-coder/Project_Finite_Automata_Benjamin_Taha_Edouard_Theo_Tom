from read import *

def is_standard(truthTable, initialStates):
    if len(initialStates) >1:
        return False
    for state in truthTable:
        for word in state:
            for target in word:
                if str(target) == initialStates[0]:
                    return False
    return True

def standardization(truthTable, initialStates):
    initial = [[] for i in range(len(truthTable[0]))]
    for i_state in initialStates:
        for i in range(len(truthTable[int(i_state)])):
            for j in range(len(truthTable[int(i_state)][i])):
                if truthTable[int(i_state)][i][j] not in initial[i]:
                    initial[i].append(truthTable[int(i_state)][i][j])
    truthTable.append(initial)
    initialStates = str(len(truthTable)-1)
    return truthTable, initialStates

def standardization_on_demand(truthTable, initialStates, finalStates):
    if not is_standard(truthTable, initialStates):
            truthTable, initialStates = standardization(truthTable, initialStates)
            printTruthTable(truthTable, initialStates, finalStates)
            return truthTable, initialStates, 1
    print("The automata is already standardized!")
    return truthTable, initialStates, 0
