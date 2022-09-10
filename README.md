# SudokuSolver
A personal project written in python that takes a sudoku input through a GUI and solves the puzzle. Even the trickiest sudoku can be solved as the program is able to make an educated guess when necessary (as shown below).

```
def solve(sudoku):
  sudoku = fill_in_any_numbers_that_are_certain(sudoku)
  if sudoku.cannot_fill_anymore AND sudoku.not_solved:
    values = pick_empty_sudoku_box_with_fewest_options(sudoku)
    for value in values:
      new_sudoku = place_value_in_sudoku(value, sudoku)
      solve(new_sudoku)
      if sudoku.solved:
        break
```

## Snippet
![image](https://user-images.githubusercontent.com/42321644/189491510-bc2fe831-9e03-4d2c-9f7b-8633313efb23.png)
        
## Requirements:
Tkinter import

## Instructions:
1. Run driver.py found in place SudokuSolver/src/driver.py using the windows console command python driver.py
2. Enter Sudoku puzzle
3. Click solve
4. Click clear to try another
