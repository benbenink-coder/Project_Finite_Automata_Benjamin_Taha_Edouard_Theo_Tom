import os
import subprocess

os.makedirs("traces", exist_ok=True)

for i in range(1, 45):
    num = f"{i:02d}"
    
    # We choose automaton i
    # 1. Standardize
    # 2. Determinize
    # 3. Complete
    # 4. Minimize (answers y to deter/compl if asked)
    # y
    # y
    # 6. Select another
    
    inputs = f"{i}\n1\n2\n3\n4\ny\ny\n6\n"
    
    try:
        process = subprocess.Popen(
            ["python3", "main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=inputs, timeout=2)
        
        with open(f"traces/trace_fa{num}.txt", "w") as f:
            f.write(stdout)
            
    except subprocess.TimeoutExpired:
        process.kill()

print("Traces generated in 'traces/' folder")
