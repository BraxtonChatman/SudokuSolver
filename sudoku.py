import tkinter as tk


def print_puzzle(puzzle):
    """Prints puzzle in individual row format"""
    for row in puzzle:
        print(row)


def has_empty(puzzle):
    """Determines if there are any empty spaces in the puzzle remaining.
    Returns False if no empty space remains, otherwise returns the indices
    for the first empty space as an ordered pair"""
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return i,j
    return False


def in_block(puzzle, index_pair):
    """Determines whether the entry at given index pair
    exists more than once in its containing 3x3 block"""
    block_indices = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    # determine the index ranges for the 3x3 block the given entry is in
    for i in block_indices:
        if index_pair[0] in i:
            x_range = i
        if index_pair[1] in i:
            y_range = i

    block = []
    for i in x_range:
        block += puzzle[i][y_range[0] : y_range[2] + 1]
    
    if block.count(puzzle[index_pair[0]][index_pair[1]]) > 1:
        return True
    else:
        return False
    

def has_conflict(puzzle, index_pair):
    """Determines if the number in the puzzle at the given index
    conflicts with the rest of the puzzle and returns boolean value"""
    
    for i in range(9):
        # check if entry exists in row already
        if i != index_pair[0]:
            if puzzle[i][index_pair[1]] == puzzle[index_pair[0]][index_pair[1]]:
                return True
        
        # check if entry exists in column already
        if i != index_pair[1]:
            if puzzle[index_pair[0]][i] == puzzle[index_pair[0]][index_pair[1]]:
                return True
        
    # check if entry exists in 3x3 block already
    if in_block(puzzle, index_pair):
        return True
    
    return False
        

def solve_puzzle(puzzle):
    """Takes in 9x9 list of integers representing a sudoku puzzle
    function attempts to fill first space (left->right, top->bottom)
    with the lowest possible number and continues to the next space.
    If it is discovered that that a number doesn't work in a space, then
    the function backtracks and increments the space."""

    # if puzzle is full, return true, or current is indices of first empty
    current = has_empty(puzzle)
    if current is False:
        return True
    
    puzzle[current[0]][current[1]] = 1
    while True:
        # prior entry is invalid
        if puzzle[current[0]][current[1]] == 10:
            puzzle[current[0]][current[1]] = 0
            return False
        
        # check if current entry is valid
        if has_conflict(puzzle, current):
            puzzle[current[0]][current[1]] += 1 # increment invalid
        else:
            solution = solve_puzzle(puzzle) # solve puzzle on remaining empty spaces
            if solution:
                return True 
            else:
                puzzle[current[0]][current[1]] += 1 # no solution for following puzzle spaces


def validate_solution(solved_puzzle):
    """Takes a completed 9x9 grid and verifies that there is
    one of each number in every column, row, and 3x3 block.
    Returns True if solution is valid, False if not"""

    # check rows
    for i in range(9):
        for j in range(1, 10):
            if j not in solved_puzzle[i]:
                return False

    # check columns     
    for i in range(9):
        column_list = []
        for j in range(9):
            column_list.append(solved_puzzle[j][i])
        for k in range(1, 10):
            if k not in column_list:
                return False

    # check 3x3 blocks
    block_ends = [(0, 3), (3, 6), (6, 9)]
    for x_range in block_ends:
        for y_range in block_ends:
            block_list = []
            for i in range(*x_range):
                block_list += solved_puzzle[i][y_range[0]:y_range[1]]

            for i in range(1, 10):
                if i not in block_list:
                    return False
      
    return True


def solve_gui(entry_list):
    """Takes the clues in the entries given by entry list
    and inputs to solve_puzzle function"""
    puzzle = []
    
    for entry_row in entry_list:
        puzzle_row = []
        for entry in entry_row:
            entry_value = entry.get()
            if entry_value == "":
                entry_value = 0
            puzzle_row.append(int(entry_value))
        puzzle.append(puzzle_row)
        puzzle_row = []

    solve_puzzle(puzzle)

    if validate_solution(puzzle):
        for row in range(9):
            for column in range(9):
                entry_list[row][column].delete(0, "end")
                entry_list[row][column].insert(0, str(puzzle[row][column]))
    else:
        return False



def sudoku_gui():
    """Function to present sudoku solver GUI with
    representation for empty puzzle and ability to input
    current clues. Calls solve_puzzle and validate_solution
    functions."""

    root = tk.Tk()
    root.geometry("450x400")
    root.title("Sudoku Solver")
    main_window = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    main_window.pack()

    # make 2D list of Entries representing number spaces on board
    entry_list = []
    for grid_row in range(9):
        entry_sublist = []
        for grid_column in range(9):
            new_entry = tk.Entry(main_window, width = 2, font = "Calibri 20")
            new_entry.grid(row = grid_row, column = grid_column, ipadx = 1)
            entry_sublist.append(new_entry)
        entry_list.append(entry_sublist)

    # row and column dividers for 3x3 blocks
    for entry in entry_list[2] + entry_list[5]:
        entry.grid_configure(pady = (0, 6))
    for i in range(9):
        entry_list[i][2].grid_configure(padx = (0, 6))
        entry_list[i][5].grid_configure(padx = (0, 6))
    
    solve_button = tk.Button(root, text = "Solve", width = 10, border = 5, command = lambda: solve_gui(entry_list))
    solve_button.pack(pady = 15)


    grid4 = [
        [0, 0, 3, 0, 0, 4, 5, 0, 2],
        [0, 5, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 8, 0, 0, 5, 3, 6, 0],
        [0, 0, 0, 2, 0, 0, 7, 4, 3],
        [2, 7, 0, 3, 0, 0, 0, 8, 0],
        [3, 4, 0, 7, 5, 0, 0, 0, 0],
        [0, 0, 5, 4, 0, 0, 0, 0, 6],
        [9, 0, 2, 0, 0, 0, 0, 5, 0],
        [4, 0, 0, 0, 0, 2, 9, 0, 0]
    ]

    for i in range(9):
        for j in range(9):
            entry_list[i][j].delete(0, "end")
            if grid4[i][j] == 0:
                entry_list[i][j].insert(0, "")
            else:
                entry_list[i][j].insert(0, str(grid4[i][j]))



    root.mainloop()


if __name__ == "__main__":
    sudoku_gui()


# Test Puzzles
grid1 = [
    [9, 2, 6, 1, 7, 8, 5, 4, 3],
    [4, 7, 3, 6, 5, 2, 1, 9, 8],
    [8, 5, 1, 9, 4, 3, 6, 2, 7],
    [6, 8, 5, 2, 3, 1, 9, 7, 4],
    [7, 3, 4, 8, 9, 5, 2, 6, 1],
    [2, 1, 9, 4, 6, 7, 8, 3, 5],
    [5, 6, 8, 7, 2, 4, 3, 1, 9],
    [3, 4, 2, 5, 1, 9, 7, 8, 6],
    [1, 9, 7, 3, 8, 6, 4, 5, 0]
]
sol1 = [
    [9, 2, 6, 1, 7, 8, 5, 4, 3],
    [4, 7, 3, 6, 5, 2, 1, 9, 8],
    [8, 5, 1, 9, 4, 3, 6, 2, 7],
    [6, 8, 5, 2, 3, 1, 9, 7, 4],
    [7, 3, 4, 8, 9, 5, 2, 6, 1],
    [2, 1, 9, 4, 6, 7, 8, 3, 5],
    [5, 6, 8, 7, 2, 4, 3, 1, 9],
    [3, 4, 2, 5, 1, 9, 7, 8, 6],
    [1, 9, 7, 3, 8, 6, 4, 5, 2]
]


grid2 = [
    [0, 0, 0, 0, 0, 1, 2, 3, 0],
    [1, 2, 3, 0, 0, 8, 0, 4, 0],
    [8, 0, 4, 0, 0, 7, 6, 5, 0],
    [7, 6, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 2, 3],
    [0, 1, 2, 3, 0, 0, 8, 0, 4],
    [0, 8, 0, 4, 0, 0, 7, 6, 5],
    [0, 7, 6, 5, 0, 0, 0, 0, 0],
] 
sol2 = [
    [6, 5, 7, 9, 4, 1, 2, 3, 8],
    [1, 2, 3, 6, 5, 8, 9, 4, 7],
    [8, 9, 4, 2, 3, 7, 6, 5, 1],
    [7, 6, 5, 1, 2, 3, 4, 8, 9],
    [2, 3, 1, 8, 9, 4, 5, 7, 6],
    [9, 4, 8, 7, 6, 5, 1, 2, 3],
    [5, 1, 2, 3, 7, 6, 8, 9, 4],
    [3, 8, 9, 4, 1, 2, 7, 6, 5],
    [4, 7, 6, 5, 8, 9, 3, 1, 2]
]


grid3 = [
    [0, 7, 5, 0, 9, 0, 0, 0, 6],
    [0, 2, 3, 0, 8, 0, 0, 4, 0],
    [8, 0, 0, 0, 0, 3, 0, 0, 1],
    [5, 0, 0, 7, 0, 2, 0, 0, 0],
    [0, 4, 0, 8, 0, 6, 0, 2, 0],
    [0, 0, 0, 9, 0, 1, 0, 0, 3],
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
]
sol3 = [
    [1, 7, 5, 2, 9, 4, 3, 8, 6],
    [6, 2, 3, 1, 8, 5, 7, 4, 9],
    [8, 9, 4, 6, 7, 3, 2, 5, 1],
    [5, 1, 6, 7, 3, 2, 4, 9, 8],
    [3, 4, 9, 8, 5, 6, 1, 2, 7],
    [2, 8, 7, 9, 4, 1, 5, 6, 3],
    [9, 3, 1, 4, 2, 8, 6, 7, 5],
    [4, 6, 8, 5, 1, 7, 9, 3, 2],
    [7, 5, 2, 3, 6, 9, 8, 1, 4]
]


grid4 = [
    [0, 0, 3, 0, 0, 4, 5, 0, 2],
    [0, 5, 0, 0, 0, 3, 0, 0, 0],
    [0, 0, 8, 0, 0, 5, 3, 6, 0],
    [0, 0, 0, 2, 0, 0, 7, 4, 3],
    [2, 7, 0, 3, 0, 0, 0, 8, 0],
    [3, 4, 0, 7, 5, 0, 0, 0, 0],
    [0, 0, 5, 4, 0, 0, 0, 0, 6],
    [9, 0, 2, 0, 0, 0, 0, 5, 0],
    [4, 0, 0, 0, 0, 2, 9, 0, 0]
]
sol4 = [
    [6, 9, 3, 1, 8, 4, 5, 7, 2],
    [7, 5, 4, 6, 2, 3, 8, 1, 9],
    [1, 2, 8, 9, 7, 5, 3, 6, 4],
    [5, 8, 1, 2, 6, 9, 7, 4, 3],
    [2, 7, 9, 3, 4, 1, 6, 8, 5],
    [3, 4, 6, 7, 5, 8, 2, 9, 1],
    [8, 3, 5, 4, 9, 7, 1, 2, 6],
    [9, 1, 2, 8, 3, 6, 4, 5, 7],
    [4, 6, 7, 5, 1, 2, 9, 3, 8]
]



grid5 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 8, 5],
    [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 1, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 7, 3],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 9],
]
