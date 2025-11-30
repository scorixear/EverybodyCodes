import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    numbers = [int(x) for x in lines[0].split(',')]
    numbers.sort()
    
    crate_list = []
    min_crates = greedy_iterative(numbers, crate_list)
    print(min_crates)



def next_crate(numbers: list[int], crate_list: list[list[int]]) -> int:
    if len(numbers) == 0:
        return len(crate_list)
    next_number = numbers[0]
    next_numbers = numbers[1:]
    
    return greedy_search(next_number, next_numbers, crate_list)
    
    return full_search(next_number, next_numbers, crate_list)

def greedy_iterative(numbers: list[int], crate_list: list[list[int]]) -> int:
    max_diff = numbers[-1] - numbers[0] + 1
    for number in numbers:
        crate_list = crate_list.copy()
        best_diff = max_diff
        best_crate = None
        for i in range(len(crate_list)):
            # check if can add to crate
            if crate_list[i][-1] < number:
                # find closest match
                diff = number - crate_list[i][-1]
                if diff < best_diff:
                    best_diff = diff
                    best_crate = i
        # no crate found, make new crate
        if best_crate is None:
            crate_list.append([number])
            continue
        # add to best crate
        crate_list[best_crate].append(number)
    return len(crate_list)

def greedy_search(number: int, numbers: list[int], crate_list: list[list[int]]) -> int:
    # filter list for possible adds:
    possible_crates = []
    for i in range(len(crate_list)):
        if crate_list[i][-1] < number:
            possible_crates.append(i)
    if len(possible_crates) == 0:
        new_crates = crate_list.copy()
        new_crates.append([number])
        return next_crate(numbers, new_crates)
    
    # find crate with closest match
    best_crate = possible_crates[0]
    best_diff = number - crate_list[best_crate][-1]
    for i in possible_crates[1:]:
        diff = number - crate_list[i][-1]
        if diff < best_diff:
            best_diff = diff
            best_crate = i
    new_crates = crate_list.copy()
    new_crates[best_crate].append(number)
    return next_crate(numbers, new_crates)

def full_search(number: int, numbers: list[int], crate_list: list[list[int]]) -> int:
    min_crates = 1000000
    
    # try adding to existing crates
    for i in range(len(crate_list)):
        if crate_list[i][-1] < number:
            new_crates = crate_list.copy()
            new_crates[i].append(number)
            min_crates = min(min_crates, next_crate(numbers, new_crates))
    # try adding a new crate
    new_crates = crate_list.copy()
    new_crates.append([number])
    min_crates = min(min_crates, next_crate(numbers, new_crates))
    return min_crates
            

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
