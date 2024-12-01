import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    rules: dict[str, list[str]] = {}
    for line in lines:
        key, values = line.split(":")
        values = values.split(",")
        rules[key] = values
    
    
    
    smallest = float("inf")
    biggest = float("-inf")
    
    for key in rules.keys():
        
        population: dict[str, int] = {}
        population[key] = 1
        
        for _ in range(20):
            new_population = {}
            for key, values in rules.items():
                for value in values:
                    new_population.setdefault(value, 0)
                    if key in population:
                        new_population[value] += population[key]
            population = new_population
        # print(population)
        total = sum(population[x] for x in population)
        smallest = min(smallest, total)
        biggest = max(biggest, total)
    print(biggest - smallest)
    
if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
