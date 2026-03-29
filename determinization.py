from read import *

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
    return sorted(list(set(arr))) #remove duplicates and sort it asc so [2,1,3] and [3,2,1] etc.. are considered same

def eps_closure(nbSymbols, truthTable, indice, epsCl):
    closure = {indice}
    stack = [indice]
    while stack:
        curr = stack.pop()
        # Ensure we access the epsilon column correctly
        for s in truthTable[int(curr)][nbSymbols]:
            if int(s) not in closure:
                closure.add(int(s))
                stack.append(int(s))
    epsCl[indice] = ".".join(str(x) for x in sorted(list(closure)))
    return epsCl[indice]

def determinize(nbSymbols, nbState, initialStates, finalStates, truthTable):
    newTruthTable = []
    toDo = []
    indicesToName = []

    needEps = False
    for row in truthTable:
        if len(row[nbSymbols]) > 0:
             #eps_closure
             needEps = True
             break
    
    if needEps:
        epsCl = ["" for i in range(nbState)]
        for i in range(nbState):
            eps_closure(nbSymbols, truthTable, i, epsCl)
        print(epsCl) 
    

    start_state = []
    if needEps:
        for s in initialStates:
            start_state.extend([int(x) for x in epsCl[int(s)].split(".") if x != ""])
    else:
        start_state = [int(x) for x in initialStates]

    newInitialStates = ["0"]
    newFinalStates = []
    
    start_state = sls(start_state)
    toDo.append(start_state)

    print(toDo)

    indice = 0
    while indice < (len(toDo)):
        stateName = ".".join(str(s) for s in toDo[indice])
        indicesToName.append(stateName)

        if any(str(e) in finalStates for e in toDo[indice]):
            newFinalStates.append(str(indice))

        stateRow = []

        for i in range(int(nbSymbols)):
            trans = [] 
            for j in toDo[indice]:
                trans.extend(truthTable[int(j)][i])

            if needEps:
                eps_trans = []
                for t in trans:
                    eps_trans.extend([int(x) for x in epsCl[int(t)].split(".") if x != ""])
                trans = sls(eps_trans)
                print(trans)
            else:
                trans = sls([int(x) for x in trans])

            if len(trans) > 0:
                if trans not in toDo:
                    toDo.append(trans)
                target_index = [toDo.index(trans)]
            else:
                target_index = []

            stateRow.append(target_index)

        stateRow.append([])
        newTruthTable.append(stateRow)
        indice +=1
    print(indicesToName)

    printTruthTable(newTruthTable, newInitialStates, newFinalStates)

    truthTable = newTruthTable
    initialStates = newInitialStates
    finalStates = newFinalStates
    return truthTable, initialStates, finalStates


