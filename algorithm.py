def _index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    return seq.index(item) if item in seq else -1


def a_star(puzzle, h):
    """Performs A* search for goal state.
    h(puzzle) - heuristic function, returns an integer
    """
    openl = [puzzle]
    closedl = []
    move_count = 0
    while len(openl) > 0:
        x = openl.pop(0)
        move_count += 1
        if x.is_solved():
            return move_count if len(closedl) > 0 else [x]

        succ = x.generate_moves()
        for move in succ:
            # have we already seen this node?
            idx_open = _index(move, openl)
            idx_closed = _index(move, closedl)
            hval = h(move)
            fval = hval + move.current_depth

            if idx_closed == -1 and idx_open == -1:
                move.heuristic_value = hval
                openl.append(move)
            elif idx_open > -1:
                copy = openl[idx_open]
                if fval < copy.heuristic_value + copy.current_depth:
                    # copy move's values over existing
                    copy.heuristic_value = hval
                    copy.parent_node = move.parent_node
                    copy.current_depth = move.current_depth
            elif idx_closed > -1:
                copy = closedl[idx_closed]
                if fval < copy.heuristic_value + copy.current_depth:
                    move.heuristic_value = hval
                    closedl.remove(copy)
                    openl.append(move)

        closedl.append(x)
        openl = sorted(openl, key=lambda p: p.heuristic_value + p.current_depth)

    # if finished state not found, return failure
    return [], 0


def is_solvable(arr):
    count = 0
    flat_puzzle = []
    for i in arr:
        flat_puzzle += i

    for i in range(8):
        for j in range(i + 1, 9):
            if flat_puzzle[j] and flat_puzzle[i] and flat_puzzle[i] > flat_puzzle[j]:
                count += 1

    return count % 2 == 0