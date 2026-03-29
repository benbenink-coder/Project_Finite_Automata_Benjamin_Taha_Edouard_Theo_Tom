# Finite Automata and Regular Expressions - Project

This project aims to provide a better understanding of Finite Automata (FA) by implementing them in Python and performing various operations on them such as determinization, completion, standardization, and minimization. It also includes word recognition testing and complementary language generation.

## Project Description

Developed by: Benjamin, Taha, Edouard, Theo, Tom
Course: EFREI P2 INT 2025/2026 – Finite Automata and Regular Expressions

The program allows a user to interactively select a finite automaton defined in a text file and explore its properties through a terminal interface. Multiple operations can be chained continuously without restarting the program.

### Key Features
1. **Reading and Displaying**: Reads an FA encoded in a `.txt` file and displays its initial state(s), terminal state(s), and transition table.
2. **Properties Checking**: Evaluates if the FA is standard, deterministic, and complete. Explanatory messages are displayed if any of these conditions are not met.
3. **Standardization**: Standardizes the automaton on demand if it is not already standard.
4. **Determinization and Completion**: Converts a non-deterministic or incomplete automaton into a Complete Deterministic Finite Automaton (CDFA). States are labeled clearly (e.g., `0.1.2`) to show their composition in terms of the original FA states.
5. **Minimization**: Computes the equivalent minimal automaton (MCDFA) from the CDFA, displaying successive partitions and the resulting equivalence table.
6. **Word Recognition Testing**: Interactively tests if user-input words are recognized by the current automaton.
7. **Complementary Language**: Generates an automaton that recognizes the complementary language of the given FA and allows word recognition testing on it.

## File Format

Automata must be described in `.txt` files in the `test_automata/` directory. The format is as follows:

```
Line 1: number of symbols in the automaton’s alphabet.
Line 2: number of states.
Line 3: number of initial states, followed by their numeric labels.
Line 4: number of final states, followed by their numeric labels.
Line 5: number of transitions.
Lines 6 and following: transitions in the form <source state><symbol><target state>
```

**Example:**
```text
2
5
1 0
1 4
6
0a0
0b0
0a1
1b2
2a3
3a4
```

## How to Run

1. **Requirements**: Python 3.x is required.
2. **Execution**: Navigate to the project root directory and run the main script in the terminal:
   ```bash
   python3 main.py
   ```
3. **Usage**:
   - The program will prompt you to select an automaton (e.g., type `8` for `test_fa08.txt`).
   - Follow the interactive terminal prompts to apply standardizations, determinization, completions, and minimizations.
   - For word testing, type the required word and press enter. To stop testing words, type `end` (or the equivalent exit string specified by the prompt).

## Project Structure

- `main.py`: The entry point for the interactive program loop.
- `read.py`: Logic to parse the `.txt` files into data structures.
- `standardization.py`: Automaton standardization algorithms.
- `determinization.py`: Converts Non-Deterministic FAs into CDFAs.
- `completion.py`: Ensures deterministic FAs are complete.
- `minimization.py`: Partitioning logic and creation of the minimal automaton.
- `words.py`: Word recognition testing logic.
- `test_automata/`: Folder containing all `.txt` representations of the FAs.
