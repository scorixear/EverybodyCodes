import os
import sys
import time
from enum import Enum
from typing import NamedTuple

import numpy as np
import numpy.typing as npt

sys.path.append(os.path.join(sys.path[0], "..", ".."))
from algorithms.dijkstra import Dijkstra


class Direction(Enum):
    """A unit step on the grid. NONE is the heading before the first move."""

    NONE = (0, 0)
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    @classmethod
    def moves(cls) -> tuple["Direction", ...]:
        return (cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    @property
    def opposite(self) -> "Direction":
        return Direction((-self.dx, -self.dy))

    def __lt__(self, other: "Direction") -> bool:
        # Needed for heap tie-breaking inside Dijkstra.
        return (self.dx, self.dy) < (other.dx, other.dy)


class Tile(Enum):
    WALL = "#"
    FLOOR = "."
    START = "S"
    END = "E"
    CITY = "@"


class Point(NamedTuple):
    x: int
    y: int

    def moved(self, direction: Direction) -> "Point":
        return Point(self.x + direction.dx, self.y + direction.dy)


class Walker(NamedTuple):
    """A node of the grid search.

    `is_origin` marks the node a leg starts from, so a leg can leave a city
    and later arrive back at that same city as a different node.
    """

    position: Point
    heading: Direction
    is_origin: bool


class Arrival(NamedTuple):
    """A key point reached with a specific heading."""

    key: int
    heading: Direction


class Grid:
    def __init__(self, lines: list[str]) -> None:
        self.width: int = len(lines[0])
        self.height: int = len(lines)
        self.walls: set[Point] = set()
        self.cities: list[Point] = []
        self.start: Point = Point(0, 0)
        self.end: Point = Point(0, 0)
        self._parse(lines)
        self._city_set: set[Point] = set(self.cities)

    @classmethod
    def from_file(cls, file_name: str) -> "Grid":
        path = os.path.join(sys.path[0], file_name)
        with open(path, "r", encoding="utf-8") as f:
            return cls(f.read().strip().split("\n"))

    def _parse(self, lines: list[str]) -> None:
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self._register(Point(x, y), Tile(char))

    def _register(self, point: Point, tile: Tile) -> None:
        match tile:
            case Tile.WALL:
                self.walls.add(point)
            case Tile.START:
                self.start = point
            case Tile.END:
                self.end = point
            case Tile.CITY:
                self.cities.append(point)
            case Tile.FLOOR:
                pass

    def contains(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def is_open(self, point: Point) -> bool:
        return self.contains(point) and point not in self.walls

    def is_city(self, point: Point) -> bool:
        return point in self._city_set


class KeyPoints:
    """Indexes the points that matter: cities are 0..n-1, then start, then end."""

    def __init__(self, grid: Grid) -> None:
        self.city_count: int = len(grid.cities)
        self.start_key: int = self.city_count
        self.end_key: int = self.city_count + 1
        self._positions: list[Point] = grid.cities + [grid.start, grid.end]

    def position(self, key: int) -> Point:
        return self._positions[key]

    def cities(self) -> range:
        return range(self.city_count)

    def is_city(self, key: int) -> bool:
        return key < self.city_count


class LegTable:
    """Shortest legal walk from an arrival to the next city (or the end).

    A leg never passes over a city, so every leg counts exactly one visit.
    """

    def __init__(self, grid: Grid, keys: KeyPoints) -> None:
        self._grid: Grid = grid
        self._keys: KeyPoints = keys
        self._dijkstra: Dijkstra[int, Walker] = Dijkstra(
            self._neighbours, self._step_cost
        )
        self.legs: dict[Arrival, dict[Arrival, int]] = self._build()

    def start_arrival(self) -> Arrival:
        return Arrival(self._keys.start_key, Direction.NONE)

    def _build(self) -> dict[Arrival, dict[Arrival, int]]:
        return {source: self._legs_from(source) for source in self._sources()}

    def _sources(self) -> list[Arrival]:
        cities = [
            Arrival(key, heading)
            for key in self._keys.cities()
            for heading in Direction.moves()
        ]
        return [self.start_arrival()] + cities

    def _targets(self) -> list[int]:
        return list(self._keys.cities()) + [self._keys.end_key]

    def _legs_from(self, source: Arrival) -> dict[Arrival, int]:
        self._dijkstra.find_path(self._walker(source, True), None)
        legs: dict[Arrival, int] = {}
        for key in self._targets():
            for heading in Direction.moves():
                arrival = Arrival(key, heading)
                cost = self._dijkstra.costs.get(self._walker(arrival, False))
                if cost is not None:
                    legs[arrival] = cost
        return legs

    def _walker(self, arrival: Arrival, is_origin: bool) -> Walker:
        return Walker(self._keys.position(arrival.key), arrival.heading, is_origin)

    def _neighbours(self, walker: Walker) -> list[Walker]:
        if self._is_leg_end(walker):
            return []
        return [
            Walker(walker.position.moved(move), move, False)
            for move in Direction.moves()
            if move != walker.heading.opposite
            and self._grid.is_open(walker.position.moved(move))
        ]

    def _is_leg_end(self, walker: Walker) -> bool:
        return not walker.is_origin and self._grid.is_city(walker.position)

    def _step_cost(self, _from: Walker, _to: Walker) -> int:
        return 1


class SlotGraph:
    """The leg table as matrices over every reachable city arrival ("slot")."""

    def __init__(self, table: LegTable, keys: KeyPoints) -> None:
        self._table: LegTable = table
        self._keys: KeyPoints = keys
        self.slots: list[Arrival] = self._collect_slots()
        self.slot_ids: dict[Arrival, int] = {s: i for i, s in enumerate(self.slots)}
        self.transitions: npt.NDArray[np.float64] = self._build_transitions()
        self.to_end: npt.NDArray[np.float64] = self._build_to_end()
        self.from_start: npt.NDArray[np.float64] = self._build_from_start()

    @property
    def size(self) -> int:
        return len(self.slots)

    def _collect_slots(self) -> list[Arrival]:
        return sorted(
            {
                target
                for row in self._table.legs.values()
                for target in row
                if self._keys.is_city(target.key)
            }
        )

    def _build_transitions(self) -> npt.NDArray[np.float64]:
        matrix = np.full((self.size, self.size), np.inf)
        for a, slot in enumerate(self.slots):
            for target, cost in self._table.legs[slot].items():
                if self._keys.is_city(target.key):
                    matrix[a, self.slot_ids[target]] = cost
        return matrix

    def _build_to_end(self) -> npt.NDArray[np.float64]:
        vector = np.full(self.size, np.inf)
        for a, slot in enumerate(self.slots):
            for target, cost in self._table.legs[slot].items():
                if target.key == self._keys.end_key:
                    vector[a] = min(vector[a], cost)
        return vector

    def _build_from_start(self) -> npt.NDArray[np.float64]:
        vector = np.full(self.size, np.inf)
        for target, cost in self._table.legs[self._table.start_arrival()].items():
            if self._keys.is_city(target.key):
                vector[self.slot_ids[target]] = cost
        return vector


class MinPlus:
    """Matrix algebra where + becomes min and * becomes +."""

    @staticmethod
    def vec_mul(
        vector: npt.NDArray[np.float64], matrix: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]:
        return (vector[:, None] + matrix).min(axis=0)


class VisitSolver:
    """Cheapest walk with exactly `visits` city visits, then on to the end."""

    def __init__(self, graph: SlotGraph, visits: int) -> None:
        self._graph: SlotGraph = graph
        self._visits: int = visits

    def solve(self) -> int:
        costs = self._graph.from_start
        for _ in range(self._visits - 1):
            costs = MinPlus.vec_mul(costs, self._graph.transitions)
        return int((costs + self._graph.to_end).min())


class Part2:
    @staticmethod
    def solve(file_name: str, visits: int) -> int:
        grid = Grid.from_file(file_name)
        keys = KeyPoints(grid)
        graph = SlotGraph(LegTable(grid, keys), keys)
        return VisitSolver(graph, visits).solve()

    @staticmethod
    def main() -> None:
        before = time.perf_counter()
        print(Part2.solve("i2.txt", 2026))
        print(f"Time: {time.perf_counter() - before:.6f}s")


if __name__ == "__main__":
    Part2.main()
