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
    with open(os.path.join(sys.path[0],"i3.txt"), "r", encoding="utf-8") as f:
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
    
    clusters: list[set[Star]] = [set()]
    cluster_connections: list[dict[Star, list[tuple[Star, int | float]]]] = [dict()]
    clusters[0].add(first_star if first_star else Star(0, 0))
    total_stars = len(stars) + 1
    while stars:
        print(f"Remaining stars: {len(stars)}/{total_stars}, clusters: {len(clusters)}")
        best_star = None
        best_cluster_star = None
        best_dist = float("inf")
        best_cluster_index = -1
        for star in stars:
            min_dist_to_cluster = float("inf")
            min_star_to_cluster = None
            min_cluster_index = -1
            for i, cluster in enumerate(clusters):
                for c in cluster:
                    dist = c.dist(star)
                    if dist < min_dist_to_cluster and dist < 6:
                        min_dist_to_cluster = dist
                        min_star_to_cluster = c
                        min_cluster_index = i
            if min_dist_to_cluster < best_dist and min_cluster_index != -1:
                best_dist = min_dist_to_cluster
                best_star = star
                best_cluster_star = min_star_to_cluster
                best_cluster_index = min_cluster_index
        if best_star and best_cluster_star and best_cluster_index != -1:
            stars.remove(best_star)
            clusters[best_cluster_index].add(best_star)
            if best_cluster_star not in cluster_connections[best_cluster_index]:
                cluster_connections[best_cluster_index][best_cluster_star] = []
            cluster_connections[best_cluster_index][best_cluster_star].append((best_star, best_dist))
        else:
            new_cluster = set()
            next_star = stars.pop()
            new_cluster.add(next_star)
            clusters.append(new_cluster)
            cluster_connections.append(dict())
    
    cluster_sizes: list[int | float] = []
    for i, c in enumerate(clusters):
        distances = sum(dist for conns in cluster_connections[i].values() for _, dist in conns)
        cluster_sizes.append(len(c) + distances)
            
    cluster_sizes.sort(reverse=True)
    print(cluster_sizes)
    largest_clusters = cluster_sizes[:3]
    total = 1
    for c in largest_clusters:
        total *= c
    print(total)



if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")
