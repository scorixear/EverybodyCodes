import heapq
from typing import Callable, Generic, TypeVar, Protocol
from typing_extensions import Self
from collections.abc import Hashable


class SupportsLessThanAndAdd(Protocol):
    def __lt__(self, other, /) -> bool: ...
    def __add__(self, other, /) -> Self: ...


T = TypeVar("T", bound=SupportsLessThanAndAdd)
H = TypeVar("H", bound=Hashable)


class AStar(Generic[T, H]):
    """Provides a generic A* algorithm implementation.

    Args:
        Generic (int | float): The cost and heuristic return type.
    """

    def __init__(
        self,
        neighbour_func: Callable[[H], list[H]],
        cost_func: Callable[[H, H], T],
        heuristic_func: Callable[[H], T],
        zeroCost: T,
    ):
        self.cost_func = cost_func
        self.neighbour_func = neighbour_func
        self.heuristic_func = heuristic_func
        self.previous: dict[H, H | None] = {}
        self.costs: dict[H, T] = {}
        self.zeroCost = zeroCost

    def find_path(self, start: H, end: H | None):
        queue = []
        queue.append([0, start])
        self.previous = {}
        self.previous[start] = None
        self.costs = {}
        self.costs[start] = self.zeroCost

        while queue:
            _, current = heapq.heappop(queue)
            if current == end:
                break
            for neighbour in self.neighbour_func(current):
                new_cost = self.costs[current] + self.cost_func(current, neighbour)
                if neighbour not in self.costs or new_cost < self.costs[neighbour]:
                    self.costs[neighbour] = new_cost
                    priority = new_cost + self.heuristic_func(neighbour)
                    heapq.heappush(queue, [priority, neighbour])
                    self.previous[neighbour] = current

    def get_cost(self, end: H) -> T | None:
        return self.costs.get(end, None)

    def get_path(self, end: H) -> list[H]:
        path = []
        current = end
        while current:
            path.append(current)
            current = self.previous[current]
        return path[::-1]
