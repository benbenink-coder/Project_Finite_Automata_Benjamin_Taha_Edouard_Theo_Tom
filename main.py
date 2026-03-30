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
        for i in range(len(automataList)):#List all the automatons
            print("{}.".format(i+1), automataList[i])
            time.sleep(0.01)
        while True:
            choiceAut = input("Input your choice (n° of the automata)\n\n") #Choose which automata to test
            try:
                choice = int(choiceAut)
                if 1 <= choice <= len(automataList):
                    break  # Exit the loop, we have a valid choice!
                else:
                    print("Error: Please choose a number between 1 and {}.".format(len(automataList)))
            except ValueError:
                print(f"Error: '{choiceAut}' is not a valid number. Please try again.")

        print("You selected automaton : {}".format(automataList[choice-1]))
        nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/"+automataList[choice-1]) #Get the information from the .txt file
        currentAutomata = [nbSymbols, nbState, initialStates, finalStates, truthTable]
        print("Below is the truth table of automaton {}".format(automataList[choice-1]))
        printTruthTable(truthTable, initialStates, finalStates)
        while True:
            while True: #Show the different operations to use on the automata
                print("\n1. Print Truth Table\n2. Standardize\n3. Determinize\n4. Complete\n5. Minimize\n6. Read Word\n7. Reset Truth Table\n8. Select another")
                
                choice_raw = input("Give the operation number: ")

                try:
                    opChoice = int(choice_raw)
                    
                    if 1 <= opChoice <= 8:
                        break 
                    else:
                        print("Error: Please choose a number between 1 and 6.")
                        
                except ValueError:
                    print(f"Error: '{choice_raw}' is not a valid number. Please try again.")
            match opChoice:
                case 1: #Print Truth Table
                    printTruthTable(truthTable, initialStates, finalStates)

                case 2: #Standardize
                    currentAutomata[-1], currentAutomata[2] = standardization_on_demand(truthTable, initialStates, finalStates) #Changes the truthTable and the initialStates, only attributes that change for standardization

                case 3: #Determinize
                    if not is_deterministic(initialStates, truthTable):
                        truthTable, initialStates, finalStates = determinize(nbSymbols, nbState, initialStates, finalStates, truthTable)
                    else:
                        print("Automaton already deterministic")

                case 4: #Complete
                    is_complete(truthTable)
                    truthTable = completion(nbSymbols, nbState, truthTable)
                    is_complete(truthTable)
                    printTruthTable(truthTable, initialStates, finalStates)

                case 5: #Minimize
                    if not is_deterministic(initialStates, truthTable):
                        det = input("The automaton isn't deterministic, do you want to determinize it ? (y/n)")
                        if det == "y":
                            truthTable, initialStates, finalStates = determinize(
                            nbSymbols,
                            nbState,
                            initialStates,
                            finalStates,
                            truthTable
                        )

                    if not is_complete(truthTable):
                        comp = input("The automaton isn't complete, do you want to complete it ? (y/n)")
                        if comp == "y":
                            truthTable = completion(nbSymbols, nbState, truthTable)
                            printTruthTable(truthTable, initialStates, finalStates)

                    MCDFA = minimization(
                        nbSymbols,
                        nbState,
                        initialStates,
                        finalStates,
                        truthTable
                    )
                    display_minimal_automaton(MCDFA, initialStates, finalStates)

                case 6: #Read word, and if wanted read for the complementary
                    read_word(nbSymbols, nbState, initialStates, finalStates, truthTable)

                    r_comp = input("Do you want to check if it can be read for the complementary ? (y/n) ")
                    if r_comp == "y":
                        workTruthTable = [row[:] for row in truthTable]
                        workInitialStates = initialStates[:]
                        workFinalStates = finalStates[:]
                        workNbState = len(workTruthTable)

                        # Determinize if needed
                        if not is_deterministic(workInitialStates, workTruthTable):
                            print("The automaton is not deterministic, determinization is required before complementary.")
                            workTruthTable, workInitialStates, workFinalStates = determinize(
                                nbSymbols,
                                workNbState,
                                workInitialStates,
                                workFinalStates,
                                workTruthTable
                            )
                            workNbState = len(workTruthTable)

                            # Complete if needed
                        if not is_complete(workTruthTable):
                            print("The automaton is not complete, completion is required before complementary.")
                            completion(nbSymbols, workNbState, workTruthTable)
                            workNbState = len(workTruthTable)

                        # Build complementary automaton
                        nbSymbolsComp, nbStateComp, initialStatesComp, compFinalStates, truthTableComp = complementary_automaton(
                            nbSymbols,
                            workNbState,
                            workInitialStates,
                            workFinalStates,
                            workTruthTable
                        )

                        read_word_comp(
                            nbSymbolsComp,
                            nbStateComp,
                            initialStatesComp,
                            compFinalStates,
                            truthTableComp)

                case 7: #Reset the Truth Table
                    nbSymbols, nbState, initialStates, finalStates, truthTable = read_txt("test_automata/" + automataList[choice - 1])

                case 8: #Choose another automata
                    break

menu()