from utils import *
initial_digits = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

initial_harder_digits = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

"""
Hard Sudoku:

4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......

"""

def grid_values(grid):
    """
    Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))




initial_sudoku = grid_values(initial_digits)
# display(temp_sudoku)

def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')

    return values

# temp_sudoku = eliminate(grid_values(initial_sudoku))
# display(temp_sudoku)

def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        # my method
        """
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for num in numbers:
            occur_box_list = []
            for box in unit:
                if num in values[box]:
                    occur_box_list.append(box)
            if len(occur_box_list)==1:
                values[occur_box_list[0]] = num
        """
        # Udacity's solution
        # List Comprehensions, less codes, consiser
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

# after_only_choice_sudoku = only_choice(temp_sudoku)
# display(after_only_choice_sudoku)

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        eliminated_sudoku = eliminate(values)

        # Use the Only Choice Strategy
        after_only_choice_sudoku = only_choice(eliminated_sudoku)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = (solved_values_before == solved_values_after)
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# display(initial_sudoku)
# stalled_values = reduce_puzzle(initial_sudoku)
# display(stalled_values)

def search(values):
    "Using depth-first search and paopagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Choose one of unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the Resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        # Copy the Sudoku to protect the original Sudoku
        # in case that there is no solution.
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


# display(search(grid_values(initial_harder_digits)))
