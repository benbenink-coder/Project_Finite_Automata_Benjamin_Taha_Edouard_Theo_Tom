

def is_complete(truthTable):
    for row in (truthTable):
        for trans in row[:-1]:  # Exclude the last column 
            if len(trans) == 0:
                print("* Complete : False")
                return False
    print("* Complete : True")
    return True

def completion(nbSymbols, nbState, truthTable):
    needSink = False
    for i in range(nbState):
        for j in range(nbSymbols): 
            if len(truthTable[i][j]) == 0:
                truthTable[i][j] = [nbState]
                needSink = True
    if needSink:
        sink_state = [[nbState] for i in range(nbSymbols)]
        # Keep the epsilon column to preserve the table shape used everywhere else.
        sink_state.append([])
        truthTable.append(sink_state)
    print("Sucessfully completed FA !")
    return truthTable