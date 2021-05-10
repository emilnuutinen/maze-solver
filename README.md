# Maze solver

A simple maze solver that uses the A* algorithm to find the shortest path through a maze.

The program prints a list of .txt files in the `mazes` folder and asks you to choose the one you want to solve.

It then tries to solve the maze with 20 moves and if that fails it tries with 150 moves and finally with 200 moves. If the maze is solved with the given maximum moves the program stops and draws the solution on the command line. 

## Requirements

Requires `Python 3.5.9` or later

## Usage

The maze files need to follow the format defined in the maze-task assignment. 

Put the maze files in the `mazes` folder and run the program in the command line with: 

```
$ python3 maze_solver.py
```
