#!/bin/bash
mkdir -p traces

echo "Generating execution traces for all 44 automata..."

for i in {1..44}; do
    # Format the number as a 2-digit number (e.g., 01, 02, ..., 44)
    num=$(printf "%02d" $i)
    
    # Automaton filename
    filename="test_fa${num}.txt"
    
    # We will simulate the user input for the menu:
    # 1. Select the automaton number ($i)
    # 2. Try an operation (e.g., 1 for Standardize, then 6 to exit)
    {
        echo "$i"       # Select automaton $i
        echo "1"        # Choose Standardize
        echo "6"        # Select another
    } | python3 main.py > "traces/trace_fa${num}.txt" 2>&1
    
    echo "Created trace_fa${num}.txt"
    
    # Optional: If you want to run more operations like determinize(2), complete(3), minimize(4) for a larger trace,
    # you can modify the inputs in the block above for each file!
done

echo "Done! All 44 execution traces are in the 'traces' folder."
