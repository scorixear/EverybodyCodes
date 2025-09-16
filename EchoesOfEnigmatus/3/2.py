import os, sys
import time
from functools import reduce
import math

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    snails = []
    for line in lines:
        x, y = map(lambda x: int(x.split("=")[1]), line.split(" "))
        snails.append((x, y))
    
    states = []
    for snail in snails:
        diag = snail[0] + snail[1] - 1
        states.append((snail[1], diag))
    total = find_alignment(states)
    print(total)
def lcm(a, b):
    return a * b // math.gcd(a, b)

def find_alignment(states):
    """
    states: list of tuples (initial_value, cycle_length)
    returns: steps until all are at value 1
    """
    cycles = []
    
    for init, cycle in states:
        # Calculate position in cycle when value is 1
        steps_to_one = (init - 1) % cycle
        
        # We need to find when (steps + steps_to_one) % cycle == 0
        # Which means we need (steps) % cycle == (cycle - steps_to_one) % cycle
        target = (cycle - steps_to_one) % cycle
        cycles.append((target, cycle))
    
    # Chinese Remainder Theorem approach
    # For simplicity, we can use the fact that:
    # For each state, we need step % cycle == target
    # The answer will be the LCM of all cycles
    
    # Calculate the LCM of all cycle lengths
    lcm_of_cycles = reduce(lcm, [cycle for _, cycle in cycles])
    
    # Start checking from step 0
    for step in range(lcm_of_cycles):
        if all((step + steps_to_one) % cycle == 0 for steps_to_one, cycle in cycles):
            return step
    
    return -1  # Should not reach here
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
