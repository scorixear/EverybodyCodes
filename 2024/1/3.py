import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"input3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        counter = 0
        for i in range(0, len(text), 3):
            counter += get_potion(text[i]) + get_potion(text[i+1]) + get_potion(text[i+2])
            number_of_creatures = sum([text[i] != 'x', text[i+1] != 'x', text[i+2] != 'x'])
            if number_of_creatures == 3:
                counter += 6
            elif number_of_creatures == 2:
                counter += 2
        print(counter)
def get_potion(creature):
    if creature == 'B':
        return 1
    elif creature == 'C':
        return 3
    elif creature == 'D':
        return 5
    return 0
                

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
