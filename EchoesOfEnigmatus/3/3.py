import os, sys
import time
from functools import reduce
import math

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
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
    equations = []
    
    for init, cycle in states:
        # For each state, we need to determine when it will have value 1
        # If initial value is init and decreasing by 1 each step,
        # we want to find step where: (init - step) % cycle == 1
        # Rearranging: step % cycle == (init - 1) % cycle
        
        remainder = (init - 1) % cycle
        equations.append((remainder, cycle))
    
    # Chinese Remainder Theorem direct solution
    result = 0
    mod_product = 1
    
    # Calculate the product of all moduli (cycle lengths)
    for _, cycle in equations:
        mod_product *= cycle
    
    for remainder, cycle in equations:
        # Calculate the partial product
        p = mod_product // cycle
        
        # Find the modular multiplicative inverse
        inv = pow(p, -1, cycle)
        
        # Update the result
        result = (result + remainder * p * inv) % mod_product
    
    return result
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
