import os, sys
import time

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def dist(self, other: "Star") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Star):
            return False
        return self.x == __o.x and self.y == __o.y


def main():
    with open(os.path.join(sys.path[0],"i2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    stars: set[Star] = set()
    first_star = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "*":
                star = Star(x, y)
                if first_star is None:
                    first_star = star
                else:
                    stars.add(star)
    
    cluster: set[Star] = set()
    cluster.add(first_star if first_star else Star(0, 0))
    connections: dict[Star, list[tuple[Star, int | float]]] = dict()
    while stars:
        best_star = None
        best_cluster_star = None
        best_dist = float("inf")
        for star in stars:
            min_dist_to_cluster = float("inf")
            min_star_to_cluster = None
            for c in cluster:
                dist = c.dist(star)
                if dist < min_dist_to_cluster:
                    min_dist_to_cluster = dist
                    min_star_to_cluster = c
            if min_dist_to_cluster < best_dist:
                best_dist = min_dist_to_cluster
                best_star = star
                best_cluster_star = min_star_to_cluster
        if best_star and best_cluster_star:
            stars.remove(best_star)
            cluster.add(best_star)
            if best_cluster_star not in connections:
                connections[best_cluster_star] = []
            connections[best_cluster_star].append((best_star, best_dist))
    total_dist = 0
    for conns in connections.values():
        for _, dist in conns:
            total_dist += dist
    print(total_dist)
    print(len(cluster))
    print(total_dist + len(cluster))
            
            
            
            



if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
