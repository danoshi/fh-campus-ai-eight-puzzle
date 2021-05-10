from copy import deepcopy
from colorama import Fore, Back, Style

dECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# unicode
left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'

bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'

first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL


def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)


class Node:
    def __init__(self, current_puzzle, previous_puzzle, g, h, d):
        self.current_puzzle = current_puzzle
        self.previous_puzzle = previous_puzzle
        self.g = g
        self.h = h
        self.d = d

    def f(self):
        return self.g + self.h


def get_position(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))


def cost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_position(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost


def getAdjNode(node):
    listNode = []
    emptyPos = get_position(node.current_puzzle, 0)

    for d in dECTIONS.keys():
        newPos = (emptyPos[0] + dECTIONS[d][0], emptyPos[1] + dECTIONS[d][1])
        if 0 <= newPos[0] < len(node.current_puzzle) and 0 <= newPos[1] < len(node.current_puzzle[0]):
            newState = deepcopy(node.current_puzzle)
            newState[emptyPos[0]][emptyPos[1]] = node.current_puzzle[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.current_puzzle, node.g + 1, cost(newState), d))

    return listNode


def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode


def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.d:
        branch.append({
            'd': node.d,
            'node': node.current_puzzle
        })
        node = closedSet[str(node.previous_puzzle)]
    branch.append({
        'd': '',
        'node': node.current_puzzle
    })
    branch.reverse()

    return branch


def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, cost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_puzzle)] = test_node

        if test_node.current_puzzle == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_puzzle) in closed_set.keys() or str(node.current_puzzle) in open_set.keys() and open_set[
                str(node.current_puzzle)].f() < node.f():
                continue
            open_set[str(node.current_puzzle)] = node

        del open_set[str(test_node.current_puzzle)]


if __name__ == '__main__':
    br = main([[7, 2, 1],
               [3, 6, 5],
               [0, 4, 8]])

    print('total steps : ', len(br) - 1)
    print()
    print(dash + dash + right_junction, "Initial Puzzle", left_junction + dash + dash)
    for b in br:
        if b['d'] != '':
            letter = ''
            if b['d'] == 'U':
                letter = 'UP'
            elif b['d'] == 'R':
                letter = "RIGHT"
            elif b['d'] == 'L':
                letter = 'LEFT'
            elif b['d'] == 'D':
                letter = 'DOWN'
            print(dash + dash + right_junction, letter, left_junction + dash + dash)
        print_puzzle(b['node'])
        print()

    print(dash + dash + right_junction, 'Solved Puzzle', left_junction + dash + dash)