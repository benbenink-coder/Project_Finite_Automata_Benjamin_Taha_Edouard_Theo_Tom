from read import *

def is_deterministic(initialStates, truthTable):
    is_det = True
    if len(initialStates) > 1: #if there are more than 1 initial states, it is not determin
        is_det = False
    else:   
        for row in (truthTable):
            for trans in row[:-1]: #exclude last transitions which contains epsilon
                if len(trans) > 1: #if it transitions to more than 1 state, it is not deterministic
                    is_det = False
                    break
            if len(row[-1]) > 0: #if it contains epsilon transitions, it is not deterministic
                    is_det = False
    print("* Deterministic : " + str(is_det))
    return is_det


#remove duplicates and sort it asc so [2,1,3] and [3,2,1] etc.. are considered same
def sls(arr):
    return sorted(list(set(arr))) 

#finds the epsilon closure and fills them directly in epsCl
def eps_closure(nbSymbols, truthTable, indice, epsCl):
    closure = {indice}
    stack = [indice]
    while stack: #as long as ther are still states reachable with epsilon
        curr = stack.pop()
        # Ensure we access the epsilon column correctly
        for s in truthTable[int(curr)][nbSymbols]: #for each state in the epsilon closure
            if int(s) not in closure:#if we discover a new reachable state
                closure.add(int(s))
                stack.append(int(s))
    epsCl[indice] = ".".join(str(x) for x in sorted(list(closure))) #the epsilon closure is the combination of all the reachable states
    return epsCl[indice]

#determinizes the automaton
# It creates a new truth table from scratch, and returns it with new state names.
# To keep track on how they were called before merging, we use indicesToName, which is displayed
def determinize(nbSymbols, initialStates, finalStates, truthTable):
    nbState = len(truthTable)
    newTruthTable = []
    toDo = []
    indicesToName = []#used to display the new names of the combined states

    #checks if the automaton has epsilon transitions
    needEps = False
    for row in truthTable:
        if len(row[nbSymbols]) > 0:
             #eps_closure
             needEps = True
             break
    
    #computes the epsilon closures if needed
    if needEps:
        epsCl = ["" for i in range(nbState)]
        for i in range(nbState):
            eps_closure(nbSymbols, truthTable, i, epsCl)

        print("\nEpsilon closures:")
        for i, group in enumerate(epsCl):
            print(f"  {i}' = {''.join(group)}")
    
    #combine all the inital states to one single
    start_state = []
    if needEps:
        for s in initialStates:
            start_state.extend([int(x) for x in epsCl[int(s)].split(".") if x != ""]) #same as brlow but we look in epsCl
    else:
        start_state = [int(x) for x in initialStates] #the new initial state is the combination of all the old initials

    newInitialStates = ["0"] #as it will w=hae only one initial state, it will always be the first one (0)
    newFinalStates = []
    
    start_state = sls(start_state)
    toDo.append(start_state)

    #main processing
    indice = 0
    while indice < (len(toDo)):
        #simply to display a more readable name 
        stateName = ".".join(str(s) for s in toDo[indice])
        indicesToName.append(stateName)

        #if it contains a final state, it is final
        if any(str(e) in finalStates for e in toDo[indice]):
            newFinalStates.append(str(indice))

        stateRow = []

        for i in range(int(nbSymbols)):
            trans = []  #contains the states we move to for a given symbol
            for j in toDo[indice]:
                trans.extend(truthTable[int(j)][i]) #it is all the states we can move to with all the states the comination is made of

            #find the states it will transition to (simply the combination)
            if needEps:
                eps_trans = []
                for t in trans:
                    eps_trans.extend([int(x) for x in epsCl[int(t)].split(".") if x != ""])#we add the epsilon closure of the states
                trans = sls(eps_trans)#sort it correctly
            else:
                trans = sls([int(x) for x in trans])#sort it correctly

            #if a new state is created, which is not processed, we add it
            if len(trans) > 0:
                if trans not in toDo:
                    toDo.append(trans) #if we "discover" a new combined state, it will be processed
                target_index = [toDo.index(trans)] #it looks in toDo for the index of the combined state 
            else:
                target_index = []#empty state (can be completed with completion)

            #we add the merged state
            stateRow.append(target_index) #we add to the row of the state the array for this symbol

        stateRow.append([]) # epsilon closure should be empty
        newTruthTable.append(stateRow)#we add this row to the new truth table
        indice +=1

    
    print("\nThe states will be renamed as follows for the determinized automaton :")
    for i, group in enumerate(indicesToName):
        print(f"{''.join(group)} -> {i}")

    printTruthTable(newTruthTable, newInitialStates, newFinalStates)
    return newTruthTable, newInitialStates, newFinalStates


