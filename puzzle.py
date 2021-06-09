import time, timeit
import copy
from heuristic import h_manhattan, h_hamming
from algorithm import a_star, is_solvable


class Puzzle:
    GOAL_STATE = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]

    def __init__(self, initial_state=None):
        self.heuristic_value = 0
        self.current_depth = 0
        self.parent_node = None
        self.adj_matrix = initial_state if initial_state else [[] for _ in range(3)]

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def _copy(self):
        return Puzzle(copy.deepcopy(self.adj_matrix))
#return all possible moves of empty space (zero puzzle)
    def _get_possible_moves(self):
        row, col = self.find(0)
        legal = []

        if row > 0:
            legal.append((row - 1, col))
        if col > 0:
            legal.append((row, col - 1))
        if row < 2:
            legal.append((row + 1, col))
        if col < 2:
            legal.append((row, col + 1))

        return legal
#taking the possible moves and generating a valid move
    def generate_moves(self):
        possible_moves = self._get_possible_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._copy()
            p.swap(a, b)
            p.current_depth = self.current_depth + 1
            p.parent_node = self
            return p

        return map(lambda puzzle_to_swap: swap_and_clone(zero, puzzle_to_swap), possible_moves)
#finds the position of the element value 
    def find(self, value):
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def get(self, row, col):
        return self.adj_matrix[row][col]

    def set(self, row, col, value):
        self.adj_matrix[row][col] = value
#swaping position of two values
    def swap(self, pos_a, pos_b):
        temp = self.get(*pos_a)
        self.set(pos_a[0], pos_a[1], self.get(*pos_b))
        self.set(pos_b[0], pos_b[1], temp)
#checking if the swapped puzzle equals the goal state 
    def is_solved(self):
        return self.adj_matrix == Puzzle.GOAL_STATE

