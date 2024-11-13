class Grid:
    def __init__(self, walls: list[tuple[int, int]], switches: list[tuple[int, int]]):
        self.walls = walls
        self.switches = switches