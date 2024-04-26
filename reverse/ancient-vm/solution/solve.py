from z3 import *

# Given constraints from the program output
constraints = []
with open("public/output.txt", "r") as f:
    results = f.read().strip().split(" ")

with open("public/program.txt", "rb") as f:
    program = f.read()

idx = 0
res_idx = 0
constraints = []
while idx < len(program):
    op = chr(program[idx])
    idx1 = program[idx + 1]
    idx2 = program[idx + 2]
    s = program[idx + 3]
    idx += 4
    args = [op, idx1, idx2, s]
    # print(args)
    if op == "h":
        args.append(program[idx])
        idx += 1
    args.append(int(results[res_idx]))
    res_idx += 1
    constraints.append(args)

# Create Z3 variables for each character in the flag
flag_chars = [BitVec(f"flag_{i}", 8) for i in range(46)]

# Create a Z3 solver
solver = Solver()

# Add constraints based on the given operations
for op, idx1, idx2, s, *args in constraints:
    c1 = flag_chars[idx1 : idx1 + s]
    c2 = flag_chars[idx2 : idx2 + s]
    if op == "x":
        solver.add(sum([a ^ b for a, b in zip(c1, c2)]) == args[0])
    elif op == "a":
        solver.add(sum([a + b for a, b in zip(c1, c2)]) == args[0])
    elif op == "s":
        solver.add(sum([a - b for a, b in zip(c1, c2)]) == args[0])
    elif op == "m":
        solver.add(sum([a * b for a, b in zip(c1, c2)]) == args[0])
    elif op == "h":
        shift_amt = args[0]
        solver.add(
            sum([(a << shift_amt) + (b >> shift_amt) for a, b in zip(c1, c2)])
            == args[1]
        )

solver.add(flag_chars[0] == ord("C"))
solver.add(flag_chars[1] == ord("C"))
solver.add(flag_chars[2] == ord("S"))
solver.add(flag_chars[3] == ord("C"))
solver.add(flag_chars[4] == ord("{"))
solver.add(flag_chars[-1] == ord("}"))

# print(solver.assertions())
# Check if the solver is satisfiable
if solver.check() == sat:
    # Get the model
    model = solver.model()
    # print(model)
    # Extract the values of the flag characters
    flag = [
        c[1]
        for c in sorted(
            [(idx, model[char].as_long()) for idx, char in enumerate(flag_chars)],
            key=lambda x: x[0],
        )
    ]
    print("".join([chr(x) for x in flag]))
