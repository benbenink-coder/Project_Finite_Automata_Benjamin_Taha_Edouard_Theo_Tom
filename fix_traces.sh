for i in 2; do
    num=$(printf "%02d" $i)
    rm "traces/trace_fa${num}.txt"
    expect run_traces_with_input.exp $i > /dev/null 2>&1
    sed -i '' 's/\r//g' "traces/trace_fa${num}.txt"
done
