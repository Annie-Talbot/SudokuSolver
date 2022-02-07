# SudokuSolver
A personal project written in python. This takes a sudoku input through a GUI, then solves the puzzle. All puzzles that can be solved, will be solved. The sudoku solver works by solving the puzzle as much as it can until it has to make a guess. The algorithm is recursive so

def solve(sudoku):
  sudoku = fill_in_any_numbers_that_are_certain(sudoku)
  if sudoku.cannot_fill_anymore AND sudoku.not_solved:
    values = pick_empty_sudoku_box_with_fewest_options(sudoku)
    for value in values:
      new_sudoku = place_value_in_sudoku(value, sudoku)
      solve(new_sudoku)
      if sudoku.solved:
        break
        
# Requirements:
Tkinter import

# Instructions:
1. Run driver.py found in place SudokuSolver/src/driver.py using the windows console command python driver.py
2. Enter Sudoku puzzle
3. Click solve
4. Click clear to try another
