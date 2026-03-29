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
