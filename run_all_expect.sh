#!/bin/bash
mkdir -p traces

echo "Generating traces including displayed user inputs using expect..."

for i in {1..44}; do
    num=$(printf "%02d" $i)
    rm -f "traces/trace_fa${num}.txt"
    # Actually EXPECT logs everything to stdout, and also writes control chars, so we use script or clean it up
    expect run_traces_with_input.exp $i > /dev/null 2>&1
    
    # We strip out Windows \r carriage returns if expect added them
    sed -i '' 's/\r//g' "traces/trace_fa${num}.txt"
    echo "Generated trace_fa${num}.txt"
done
