from typing import Iterable
import heapq


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Distance to start node
        self.h = 0  # Distance to end node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end):

    # Create start & end nodes
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize open and closed lists
    open_list = []
    closed_list = []

    # Heapify the open_list and add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # get the adjacent nodes
    adjacent_nodes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for next_position in adjacent_nodes:

            # Get node position
            node_position = (
                current_node.position[0] + next_position[0], current_node.position[1] + next_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # Manhattan distance to end node
            child.h = abs(child.position[0] - end_node.position[0]) + \
                abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    return None


def read_maze_file(file):
    with open(file, "r") as f:
        maze = f.read().splitlines()
    return maze


def create_maze_matrix(maze):

    matrix = []
    exits = []

    # Transform the maze into a matrix
    for line in maze:
        matrix.append([line[i:i+1] for i in range(0, len(line), 1)])

    # Find starting point
    start = [[(i, j) for j, cell in enumerate(row) if cell == '^']
             for i, row in enumerate(matrix) if '^' in row][0][0]

    # Find all ending points
    exits.append([(i, j) for i, row in enumerate(matrix)
                  for j, col in enumerate(row) if col == 'E'])

    # Change maze characters into numbers
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == '#':
                matrix[row][col] = 1
            elif matrix[row][col] == ' ':
                matrix[row][col] = 0
            elif matrix[row][col] == '^':
                matrix[row][col] = 0
            elif matrix[row][col] == 'E':
                matrix[row][col] = 0

    return matrix, start, exits


def print_results(path, maze, max_moves):

    # Print the path only if there is a way out from the maze
    if isinstance(path, Iterable):
        for step in path:
            maze[step[0]][step[1]] = 2

        print()
        for row in maze:
            line = []
            for col in row:
                if col == 1:
                    line.append("\u2588")
                elif col == 0:
                    line.append(" ")
                elif col == 2:
                    line.append("\u00b7")
            print("".join(line))

        if len(path) <= max_moves:
            print(
                f'Congratulations! Pentti got out from the maze in {len(path)-1} moves.')

        # Print if max_moves is not enough to get out of the maze
        else:
            print(
                f'{max_moves} moves is not enough to get out from the maze. You need {len(path)-1} moves to get out.')

    else:
        print("The exit is unreachable.")


def main():
    # Read the maze file, create the maze matrix and find the starting point and all the exit points
    maze = read_maze_file('mazes/maze-task-fourth.txt')
    maze_matrix, start, exits = create_maze_matrix(maze)

    # Get paths for all exits
    path = []
    for i, index in enumerate(exits):
        for col, j in enumerate(index):
            path.append(astar(maze_matrix, start, index[col]))

    # Find the closest exit
    if len(path) > 0:
        closest_exit = path[0]
        if isinstance(path, Iterable) and isinstance(closest_exit, Iterable):
            for i in range(0, len(path)):
                if(len(path[i]) <= len(closest_exit)):
                    closest_exit = path[i]

        # Print path for the closest exit
        print_results(closest_exit, maze_matrix, 200)
    else:
        print('Your maze is missing the exit.')


if __name__ == "__main__":
    main()
