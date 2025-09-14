import os, sys
import time
from typing import Callable

def main():
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
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
    
    steps = 256
    max_score = find_rotations(rotations, cat_face_counter, cat_faces, steps, max)
    min_score = find_rotations(rotations, cat_face_counter, cat_faces, steps, min)
    print(max_score, min_score)



def find_rotations(
    rotations: list[int],
    max_values: list[int],
    cat_faces: list[list[str]],
    rotation_amounts: int,
    decider_fn: Callable[[int, int, int], int]) -> int:
    
    dp = dict()
    stack = []
    stack.append(( [0]*len(cat_faces), rotation_amounts))
    while stack:
        indexes, rot_amt = stack.pop()
        key = (tuple(indexes), rot_amt)
        if key in dp:
            continue
        if rot_amt == 0:
            dp[key] = 0
            continue
        
        no_action_indexes = right_lever(indexes, rotations, max_values)
        pull_indexes = right_lever(pull(indexes, max_values), rotations, max_values)
        push_indexes = right_lever(push(indexes, max_values), rotations, max_values)
        
        next_keys = [
            (tuple(no_action_indexes), rot_amt-1),
            (tuple(pull_indexes), rot_amt-1),
            (tuple(push_indexes), rot_amt-1)
        ]
        
        if any(k not in dp for k in next_keys):
            stack.append((indexes, rot_amt))
            for k in next_keys:
                if k not in dp:
                    stack.append(k)
            continue
        no_action_coins = get_coins(get_cat_faces(cat_faces, no_action_indexes))
        pull_coins = get_coins(get_cat_faces(cat_faces, pull_indexes))
        push_coins = get_coins(get_cat_faces(cat_faces, push_indexes))
        no_action_continue = no_action_coins + dp[(tuple(no_action_indexes), rot_amt-1)]
        pull_continue = pull_coins + dp[(tuple(pull_indexes), rot_amt-1)]
        push_continue = push_coins + dp[(tuple(push_indexes), rot_amt-1)]
        score = decider_fn(no_action_continue, pull_continue, push_continue)
        dp[key] = score
    return dp[(tuple([0]*len(cat_faces)), rotation_amounts)]
    
    
def right_lever(indexes: list[int], rotations: list[int], max_values: list[int]) -> list[int]:
    return [(indexes[i] + rotations[i]) % max_values[i] for i in range(len(indexes))]

def pull(indexes: list[int], max_values: list[int]) -> list[int]:
    return [(indexes[i] + 1) % max_values[i] for i in range(len(indexes))]
def push(indexes: list[int], max_values: list[int]) -> list[int]:
    return [(indexes[i] - 1) % max_values[i] for i in range(len(indexes))]

def get_cat_faces(cat_faces: list[list[str]], indexes: list[int]) -> list[str]:
    return [cat_faces[i][indexes[i]] for i in range(len(cat_faces))]
    
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
