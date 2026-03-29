from read import *

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




def complementary_automaton(A):
    # Read the automaton from file A
    nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt(A)

    # Build the new final states:
    # all non-final states become final
    compFinalStates = []

    for state in range(nbState):
        if str(state) not in finalStates:
            compFinalStates.append(str(state))

    # Return the complementary automaton
    return nbSymbols, nbState, initialStates, compFinalStates, truthTable


def recognize_word_comp(word, A):
    # Read the complementary automaton
    nbSymbols, nbState, initialStates, finalStates, truthTable = complementary_automaton(A)

    # Start at the initial state
    current_state = int(initialStates[0])

    # Read the word letter by letter
    for letter in word:
        # Convert a letter into a column number
        column = ord(letter) - 97

        # If the letter is not in the alphabet, reject
        if column < 0 or column >= nbSymbols:
            return False

        # If no transition exists, reject
        if len(truthTable[current_state][column]) == 0:
            return False

        # Move to the next state
        current_state = truthTable[current_state][column][0]

    # At the end, check if the state is final in the complementary automaton
    return str(current_state) in finalStates


def read_word_comp(A):
    print("The complementary automaton is built from A.")

    word = input("Type a word to test on the complementary automaton (or 'end' to stop): ")

    while word != "end":
        if recognize_word_comp(word, A):
            print("Yes")
        else:
            print("No")

        word = input("Type a word to test on the complementary automaton (or 'end' to stop): ")
