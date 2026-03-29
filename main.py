import os
from queue import Empty
import time

from completion import *
from standardization import *
from read import *
from determinization import *
from minimization import *
from words import *

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
        while True:
            choiceAut = input("Input your choice (n° of the automata)\n\n")
            try:
                choice = int(choiceAut)
                if 1 <= choice <= len(automataList):
                    break  # Exit the loop, we have a valid choice!
                else:
                    print("Error: Please choose a number between 1 and {}.".format(len(automataList)))
            except ValueError:
                print(f"Error: '{choiceAut}' is not a valid number. Please try again.")

        print("You selected automaton : {}".format(automataList[choice-1]))
        nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/"+automataList[choice-1])
        currentAutomata = [nbSymbols, nbState, initialStates, finalStates, truthTable]
        print("Below is the truth table of automaton {}".format(automataList[choice-1]))
        printTruthTable(truthTable, initialStates, finalStates)
        while True:
            while True:
                print("\n1. Standardize\n2. Determinize\n3. Complete\n4. Minimize\n5. Read Word\n6. Select another")
                
                choice_raw = input("Give the operation number: ")

                try:
                    opChoice = int(choice_raw)
                    
                    if 1 <= opChoice <= 6:
                        break 
                    else:
                        print("Error: Please choose a number between 1 and 6.")
                        
                except ValueError:
                    print(f"Error: '{choice_raw}' is not a valid number. Please try again.")
            match opChoice:
                case 1:
                    currentAutomata[-1], currentAutomata[2] = standardization_on_demand(truthTable, initialStates, finalStates)
                case 2: 
                    if not is_deterministic(initialStates, truthTable):
                        determinize(nbSymbols, nbState, initialStates, finalStates, truthTable)
                    else:
                        print("automaton already deterministic")
                case 3:
                    is_complete(truthTable)
                    completion(nbSymbols, nbState, truthTable)
                    is_complete(truthTable)
                    printTruthTable(truthTable, initialStates, finalStates)
                case 4:
                    workTruthTable = truthTable
                    workInitialStates = initialStates
                    workFinalStates = finalStates

                    if not is_deterministic(workInitialStates, workTruthTable):
                        det = input("The automaton isn't deterministic, do you want to determinize it ? (y/n)")
                        if det != "y":
                            continue
                        workTruthTable, workInitialStates, workFinalStates = determinize(
                            nbSymbols,
                            len(workTruthTable),
                            workInitialStates,
                            workFinalStates,
                            workTruthTable,
                        )

                    if not is_complete(workTruthTable):
                        comp = input("The automaton isn't complete, do you want to complete it ? (y/n)")
                        if comp != "y":
                            continue
                        completion(nbSymbols, len(workTruthTable), workTruthTable)
                        printTruthTable(workTruthTable, workInitialStates, workFinalStates)

                    MCDFA = minimization(
                        nbSymbols,
                        len(workTruthTable),
                        workInitialStates,
                        workFinalStates,
                        workTruthTable,
                    )
                    display_minimal_automaton(MCDFA, workInitialStates, workFinalStates)
                case 5:
                    read_word(nbSymbols, nbState, initialStates, finalStates, truthTable)
                    r_comp = input("Do you want to check if it can be read for the complementary ? (y/n)")
                    if r_comp == "y":
                        nbSymbols, nbState, initialStates, compFinalStates, truthTable = complementary_automaton(nbSymbols, nbState, initialStates, finalStates, truthTable)
                        read_word_comp(nbSymbols, nbState, initialStates, compFinalStates, truthTable)
                case 6:
                    break

menu()