#!/bin/bash
mkdir -p traces

echo "Generating traces including Read Word without the bad 'y's..."

for i in {1..44}; do
    num=$(printf "%02d" $i)
    
    # We remove the 'y' answers because after steps 2 (determinize) and 3 (complete), 
    # step 4 (minimize) sees that it's already deterministic and complete, so it 
    # doesn't prompt for 'y'.
    echo -e "$i\n1\n2\n3\n4\n5\naba\nend\n6\n" | python3 main.py > traces/trace_fa${num}.txt 2>/dev/null
    
    echo "Generated trace_fa${num}.txt"
done
