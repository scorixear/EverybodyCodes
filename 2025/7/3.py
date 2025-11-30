import os, sys
import time

total_names = set()


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    names = lines[0].split(",")
    rules = {}
    for line in lines[2:]:
        parts = line.split(" > ")
        followers = parts[1].split(",")
        rules[parts[0]] = set(followers)
    for name in names:
        curr_pos = 0
        matched = True
        while curr_pos < len(name) - 1:
            rule = rules.get(name[curr_pos])
            if rule is None or name[curr_pos + 1] not in rule:
                matched = False
                break
            curr_pos += 1
        if matched:
            get_total(name, rules)
    print(len(total_names))
    # total_names.sort(key=lambda x: (len(x), x))
    # for name in total_names:
    #     print(name)


def get_total(name: str, rules: dict[str, set[str]]):
    return dfs(name[len(name) - 1], rules, len(name), name)


def dfs(char: str, rules: dict[str, set[str]], length: int, name: str):
    if length == 11:
        return
    followers = rules.get(char)
    if followers is None:
        return
    total = 0
    if length >= 6:
        for follower in followers:
            total_names.add(name + follower)
    for follower in followers:
        dfs(follower, rules, length + 1, name + follower)
    return total


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
