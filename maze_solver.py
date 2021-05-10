from typing import Iterable
import heapq
import os


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Distance to start node
        self.h = 0  # Distance to end node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    # defining less than for the heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for the heap queue
    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return the reversed path


def astar(maze, start, end):

    # Create start & end nodes
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize open & closed lists
    open_list = []
    closed_list = []

    # Heapify the open_list and add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # get the adjacent nodes
    adjacent_nodes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # Loop until you find the end node
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Return the path if end node is found
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for next_position in adjacent_nodes:

            # Get node position
            node_position = (
                current_node.position[0] + next_position[0], current_node.position[1] + next_position[1])

            # Make sure were inside the maze
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # check for walls
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Check if the child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values (Manhattan distance)
            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + \
                abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    # Return None if the exit is unreachable
    return None


# Open and read the maze file
def read_maze_file(file):
    with open(file, "r") as f:
        maze = f.read().splitlines()
    return maze


# Transform the matrix into a numerical form and find the start point and ending points
def create_maze_matrix(maze):

    matrix = []
    exits = []

    # Transform the maze into a matrix
    for line in maze:
        matrix.append([line[i:i+1] for i in range(0, len(line), 1)])

    # Find the starting point
    start = [[(i, j) for j, cell in enumerate(row) if cell == '^']
             for i, row in enumerate(matrix) if '^' in row][0][0]

    # Find all the ending points
    exits.append([(i, j) for i, row in enumerate(matrix)
                  for j, col in enumerate(row) if col == 'E'])

    # Change maze characters into numbers
    # Wall is 1, everything else is 0
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


def draw_finished_maze(path, maze):

    # Add path to the maze
    for step in path:
        maze[step[0]][step[1]] = 2

    # Print the finished maze
    print()
    for row in maze:
        line = []
        for col in row:
            if col == 1:
                # Full size block represents wall
                line.append("\u2588")
            elif col == 0:
                # Movable space
                line.append(" ")
            elif col == 2:
                # Centered dot represents the path
                line.append("\u00b7")
        print("".join(line))


def get_results(maze):

    # Create the numerical maze matrix, starting point for Pentti and all the exit points
    maze_matrix, start, exits = create_maze_matrix(maze)

    # Create a list of max moves
    max_moves = [20, 150, 200]

    # Get paths for all exits
    path = []
    for i, index in enumerate(exits):
        for col, j in enumerate(index):
            path.append(astar(maze_matrix, start, index[col]))

    # Find the closest exit if the maze is solvable
    if len(path) > 0:
        closest_exit = path[0]
        if isinstance(path, Iterable) and isinstance(closest_exit, Iterable):
            for i in range(0, len(path)):

                # Stop the program if the maze has a wrong format
                if (path[i] == None or closest_exit == None):
                    print('The maze file has a wrong format.')

                    return

                elif (len(path[i]) <= len(closest_exit)):
                    closest_exit = path[i]

            # Test the maze with the defined max moves
            for move in max_moves:
                # If the maze is unsolvable with the current max moves
                if len(closest_exit)-1 >= move:
                    print(f'Trying the maze with {move} moves.')
                    print(f'FAIL. The maze is unsolvable in {move} moves.')
                    print()

                # Else print the results
                else:
                    print(f'Trying the maze with {move} moves.')
                    print(
                        f'PASS! Pentti got out of the maze in {len(closest_exit)-1} moves!')
                    draw_finished_maze(closest_exit, maze_matrix)

                    return

            return

        else:
            print("The exit is unreachable.")

    else:
        print('Your maze is missing the exit.')


def main():

    # Get mazes form the mazes folder
    mazes = []
    print()
    for i, file in enumerate(os.listdir('mazes')):
        if file.endswith(".txt"):
            mazes.append(file)
            print(f'{i}) {file}')

    # Ask for users choice
    print()
    choice = int(
        input('Give the number of the maze you want to solve: '))
    print()

    # Get the full path for the selected file
    selected_file = os.path.join("mazes", mazes[choice])

    # Read the maze file, create the maze matrix and find the starting point and all the exit points
    maze = read_maze_file(selected_file)
    get_results(maze)


if __name__ == "__main__":
    main()
