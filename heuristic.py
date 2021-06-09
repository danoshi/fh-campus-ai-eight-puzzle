#Here all the Heristic will be defined and calculated
def _heuristic(puzzle, item_total_calc, total_calc):
    """
    Heuristic template that provides the current and target position for each number and the
    total function.

    Parameters:
    puzzle - the puzzle
    item_total_calc - takes 4 parameters: current row, target row, current col, target col.
    Returns int.
    total_calc - takes 1 parameter, the sum of item_total_calc over all entries, and returns int.
    This is the value of the heuristic function
    """
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.get(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0:
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)

#returning manhattan heurisitic 
def h_manhattan(puzzle):
    return _heuristic(puzzle,
                      lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                      lambda t: t)


def hamming(row, target_row, column, target_column):
    if row != target_row or column != target_column:
        return 1
    return 0

#returning hamming heurisitic 
def h_hamming(puzzle):
    return _heuristic(puzzle,
                      hamming,
                      lambda t: t)