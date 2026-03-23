# Project_Finite_Automata_Benjamin_Taha_Edouard_Theo_Tom

The goal of this project is to get a better understanding of Finite Automatas, by implementing them in a programming language (here, python) and applying operations over them (minimization, standardization, etc...)

Firstly, we had to come with a way to represent graphical FA in a text format (.txt)

We will use the given format : 

```
Line 1: number of symbols in the automaton’s alphabet.
Line 2: number of states.
Line 3: number of initial states, followed by their numeric labels.
Line 4: number of final states, followed by their numeric labels.
Line 5: number of transitions.
Lines 6 and the following lines: transitions in the form
<source state><symbol><target state >
```

And we'll store the data in Python in a Matrix (of size numberState*numberSymbols).

In the following manner : 
array[nb of states][symbolNumber(a=0,z=26)] 
at the beginning we fill everything with Xs 
to get the transition from 0 with d :
arr[0][4] = next node.

To translate a into a number, we'll use the ascii table.

## Minimization

We also implemented the minimization of a finite automaton.

This operation is applied on a complete deterministic finite automaton (CDFA), in order to obtain an equivalent automaton with the smallest possible number of states (MCDFA).

The method used is based on partitioning the states:

Firstly, we separate the states into two groups:
- final states
- non-final states

Then, we refine these groups by comparing their transitions:
states are grouped together if they behave the same way for all symbols.

This process is repeated until no more changes occur in the partition.

Finally, we build the minimal automaton:
- each group becomes a new state
- transitions are defined between these new states
- initial and final states are updated accordingly

The program also displays:
- the successive partitions
- the transitions between groups
- the correspondence between the new states and the original states
