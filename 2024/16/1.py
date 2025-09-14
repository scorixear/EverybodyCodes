import os, sys
import time

def main():
    with open(os.path.join(sys.path[0],"i1.txt"), "r", encoding="utf-8") as f:
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
    result_faces = spin(rotations, cat_face_counter, 100)
    result = " ".join([cat_faces[i][result_faces[i]] for i in range(len(cat_faces))])
    print(result)

def spin(rotations: list[int], max_values: list[int], amount: int) -> list[int]:
    new_rotations = [0 for _ in range(len(rotations))]
    for i, rot in enumerate(rotations):
        new_rotations[i] = (rot*amount) % max_values[i]
    return new_rotations
    

if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
