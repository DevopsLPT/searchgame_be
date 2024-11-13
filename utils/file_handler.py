from components.node import Node
from components.grid import Grid

def read_file(file_name: str) -> tuple[Node, Grid]:
    with open(file=file_name, mode="r") as fi:
        stone_weights = list(map(int, fi.readline().split()))
        walls, switches, ares, stones = [], [], None, []

        for r, row in enumerate(fi):
            for c, cell in enumerate(row):
                match cell:
                    case '#':
                        walls.append((r, c))
                    case '.':
                        switches.append((r, c))
                    case '@':
                        ares = (r, c)
                    case '$':
                        stones.append((r, c, stone_weights.pop(0)))
                    case '*':
                        switches.append((r, c))
                        stones.append((r, c, stone_weights.pop(0)))
                    case '+':
                        ares = (r, c)
                        switches.append((r, c))

    return (
        Node(ares=ares, stones=stones),
        Grid(walls=walls, switches=switches)
    )

def write_file(file_name: str, search_algo: str, node_count: int, goal_node: Node | None, memory_used: float = 0.0, elapsed_time: float = 0.0, write_mode: str = "w"):
    with open(file=file_name, mode=write_mode) as fo:
        weight = goal_node.weight if goal_node else 0
        path = goal_node.get_path() if goal_node else ""

        print(
            "{0}\nSteps: {1}, Weight: {2}, Node: {3}, Time (ms): {4:.2f}, Memory (MB): {5:.2f}\n{6}".format(
                search_algo, len(path), weight, node_count, elapsed_time, memory_used, path
            ), file=fo
        )
