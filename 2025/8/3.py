import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "i3.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    nums = [int(x) for x in lines[0].split(",")]
    nails = 256
    connections: dict[int, list[int]] = {}
    for smaller in range(nails + 1):
        connections[smaller] = []
    curr = nums[0]
    for num in nums[1:]:
        connections[num].append(curr)
        connections[curr].append(num)
        curr = num
    max_cuts = 0
    for smaller in range(1, nails + 1):
        for larger in range(smaller + 1, nails + 1):
            curr_cuts = 0
            # cuts = []
            for idx in range(smaller + 1, larger + 1):
                for con in connections[idx]:
                    if (
                        (idx != larger and (con < smaller or con > larger))
                        or (con == smaller and idx == larger)
                        or (con == larger and idx == smaller)
                    ):
                        curr_cuts += 1
                        # cuts.append((idx, con))
            max_cuts = max(max_cuts, curr_cuts)
            # print(f"New max cuts {max_cuts} between {smaller} and {larger}")
            # print("Cuts:", cuts)
    print(max_cuts)


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
