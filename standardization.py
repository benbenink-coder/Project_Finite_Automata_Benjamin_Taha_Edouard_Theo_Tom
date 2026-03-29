from read import *

def is_standard(truthTable, initialStates):
    '''
    Takes in parameter the truth table of an automaton and the initial states of this automaton.
    Returns if the automaton is standard (True) or not (False).
    '''
    if len(initialStates) >1: #Verify there is only one initial state
        return False
    for state in truthTable: #Verify no other states points toward the initial state
        for word in state:
            for target in word:
                if str(target) == initialStates[0]:
                    return False
    return True

def standardization(truthTable, initialStates):
    '''
    Takes in parameter the truth table of an automaton and the initial states of this automaton.
    Returns the truth table and the initial state after standardization.
    '''
    initial = [[] for i in range(len(truthTable[0]))] #Line of the truth table for the new state
    for i_state in initialStates: #Go through all initial states to append its values into the new initial state
        for i in range(len(truthTable[int(i_state)])):
            for j in range(len(truthTable[int(i_state)][i])):
                if truthTable[int(i_state)][i][j] not in initial[i]: #Verify there is no duplicates in the state's truth table
                    initial[i].append(truthTable[int(i_state)][i][j])
    truthTable.append(initial) #Add the initial state line in the truth table
    initialStates = str(len(truthTable)-1) #Update the initial states
    return truthTable, initialStates

def standardization_on_demand(truthTable, initialStates, finalStates):
    '''
    Takes in parameter the truth table of an automaton and the initial states of this automaton.
    Standardizes the automaton if necessary, and returns the truth table and the initial state after standardization.
    '''
    if not is_standard(truthTable, initialStates): #Check if the automaton is standardized
            truthTable, initialStates = standardization(truthTable, initialStates)
            printTruthTable(truthTable, initialStates, finalStates) #Print the updated truth table
            return truthTable, initialStates
    print("The automata is already standardized!")
    return truthTable, initialStates