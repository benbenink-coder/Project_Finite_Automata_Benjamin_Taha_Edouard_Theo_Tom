from read import * 
def normalize_truthTable_for_cdfa(truthTable):
    # Convert temporary sink (-1) into real sink index and enforce determinism
    normalizedTruthTable = []
    sinkIndex = len(truthTable) - 1

    for row in truthTable:
        newRow = []
        for trans in row[:-1]:
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

        # Keep the trailing column used by printTruthTable for the '*' header.
        newRow.append([])

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


def display_minimal_automaton(MCDFA, initialStates, finalStates):
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

    printTruthTable(truthTable, initialStates, finalStates)