

def is_complete(truthTable):
    for row in (truthTable):
        for trans in row[:-1]:  # Exclude the last column 
            if len(trans) == 0: #if any state has a transtion going to nowhere, it is not complete
                print("* Complete : False")
                return False
    print("* Complete : True")
    return True

def completion(nbSymbols, truthTable):
    nbState = len(truthTable)
    needSink = False
    for i in range(nbState):
        for j in range(nbSymbols): 

            if len(truthTable[i][j]) == 0:
                truthTable[i][j] = [nbState] #the sink state is located at the end of the array
                needSink = True
    if needSink:
        sink_state = [[nbState] for i in range(nbSymbols)] #creates the row for the sink state
        # Keep the epsilon column to preserve the table shape used everywhere else.
        sink_state.append([])
        truthTable.append(sink_state)
    print("Sucessfully completed FA !")
    return truthTable