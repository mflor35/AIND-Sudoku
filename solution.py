import re
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ s+t for s in A for t in B ]

boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
column_units = [cross(rows, col) for col in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_down = [['A1','B2','C3','D4','E5','F6','G7','H8','I9']]
diagonal_up = [['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist = row_units + column_units + square_units + diagonal_down + diagonal_up
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    double_values = [s for s in boxes if len(values[s]) == 2]
    nts = []
    [nts.append(s) for s in double_values for peer in peers[s] if values[s] == values[peer] and s not in nts]
    print(nts)
    for nt in nts:
        digits = values[nt]
        for peer in peers[nt]:
            if len(values[peer]) > 2:
                for d in digits:
                    values[peer] = values[peer].replace(d,'')
    return values
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    sudoku_dict = {}
    assert len(grid) == 81
    
    for i in range(len(boxes)):
        if grid[i] == '.':
            sudoku_dict[boxes[i]] = '123456789'
        else:
            sudoku_dict[boxes[i]] = grid[i]
    return sudoku_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line  = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'cf':
            print(line)
    return

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
    present_values = []
    for box in values.keys():
        if len(values[box]) == 1:
            present_values.append(box)

    for box in present_values:
        number = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(number,"")

    return values

def only_choice(values):
    """
    Finalize all the values that are the only choice for a unit.
    
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args: 
        Sudoku in dictionary form
    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    new_values = values.copy()
    for unit in unitlist:
        for digit in '123456789':
            multilocation = [box for box in unit if digit in values[box]]
            if len(multilocation) == 1:
                new_values[multilocation[0]] = digit 

    return new_values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use Eliminate Strategy
        values = eliminate(values)
        # Use Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku"
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not false). returnt the answer
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    
    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #test_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
