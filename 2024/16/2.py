import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    rotations = [int(x) for x in lines[0].split(',')]
    cat_faces: list[list[str]] = []
    cat_face_counter = []
    for line in lines[2:]:
        faces = [line[i:i+3] for i in range(0, len(line) - 2, 4)]
        for i in range(len(faces)):
            if len(cat_faces) <= i:
                cat_faces.append([])
                cat_face_counter.append(0)
            if faces[i].strip() != "":
                cat_faces[i].append(faces[i])
                cat_face_counter[i] += 1
    coins = find_rotations(rotations, cat_face_counter, cat_faces, 202420242024)
    
    print(coins)

def smallest_common_multiple(nums: list[int]) -> int:
    multiple = 1
    for n in nums:
        multiple = (multiple*n)//gcd(multiple, n)
    return multiple
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def find_rotations(rotations: list[int], max_values: list[int], cat_faces: list[list[str]], rotation_amounts: int) -> int:
    scm = smallest_common_multiple(max_values)
    scm_amounts = [0]
    for i in range(1, scm+1):
        curr_cat_faces = [cat_faces[j][(rotations[j]*i) % max_values[j]] for j in range(len(cat_faces))]
        coins = get_coins(curr_cat_faces)
        scm_amounts.append(scm_amounts[i-1] + coins)
    if scm > rotation_amounts:
        return scm_amounts[rotation_amounts]
    full_cycles = rotation_amounts // scm
    remainder = rotation_amounts % scm
    return scm_amounts[scm]*full_cycles + scm_amounts[remainder]
    
    
def get_coins(cat_faces: list[str]) -> int:
    total = "".join([face[0] + face[2] for face in cat_faces])
    occurences = dict()
    for char in total:
        if char not in occurences:
            occurences[char] = 0
        occurences[char] += 1
    total = 0
    for val in occurences.values():
        if val >= 3:
            total += val - 2
    return total


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
