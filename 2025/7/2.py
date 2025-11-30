import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    names = lines[0].split(",")
    rules = {}
    for line in lines[2:]:
        parts = line.split(" > ")
        followers = parts[1].split(",")
        rules[parts[0]] = set(followers)
    total = 0
    for i, name in enumerate(names):
        curr_pos = 0
        matched = True
        while curr_pos < len(name) - 1:
            rule = rules.get(name[curr_pos])
            if rule is None or name[curr_pos + 1] not in rule:
                matched = False
                break
            curr_pos += 1
        if matched:
            total += i + 1
    print(f"Total: {total}")


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
