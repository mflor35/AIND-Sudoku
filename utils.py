def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ s+t for s in A for t in B ]

rows = 'ABCDEFGHI' 
cols = '123456789' 
boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
column_units = [cross(rows, col) for col in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_down = [[''.join(s) for s in zip(rows,cols)]]
diagonal_up = [[''.join(s) for s in zip(rows,cols[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_down + diagonal_up
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
