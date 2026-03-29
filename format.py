import re

for i in range(1, 45):
    fname = f"traces/trace_fa{i:02d}.txt"
    try:
        with open(fname, "r") as f:
            content = f.read()
            
        # Clean up weird pexpect interlacing like '2\n8. test_fa08...'
        for d in range(1, 45):
            content = re.sub(rf"{d}\R(?=\d+\.)", f"\n", content)
            
        # Add the typed choices logically to the lines that ask for it
        content = re.sub(r"(Give the operation number:) \n(?=\d)", r"\1 \2\n", content)
        
        with open(fname, "w") as f:
            f.write(content)
    except:
        pass
