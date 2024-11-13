import heapq
import utils.funtions as funtions
from components.node import Node
from components.grid import Grid

def ucs(init_node: Node, grid: Grid):
    frontier = []
    explored = {}
    node_count = 0
    
    heapq.heappush(frontier, (init_node.weight, init_node))
    
    while frontier:
        _, current_node = heapq.heappop(frontier)
        
        explored[current_node.get_state()] = current_node.weight
        
        if funtions.is_goal(current_node, grid):
            return node_count, current_node

        for successor_node in funtions.get_successor_nodes(current_node, grid):
            state = successor_node.get_state()

            if state in explored and explored[state] <= successor_node.weight:
                continue
            
            heapq.heappush(frontier, (successor_node.weight, successor_node))
            explored[state] = successor_node.weight
            node_count += 1

    return node_count, None  
