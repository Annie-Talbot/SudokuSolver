import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from sudoku.sudoku import Sudoku

SUDOKU = [[], [], [], [], [], [], [], [], []]
""" 9x9 array[Combobox]:   Array holding the GUI widgets that represent each
                           cell of the sudoku puzzle.
"""
WINDOW = tk.Tk()
""" Tk: Tkinter GUI window.
"""


def update_gui(sudoku: Sudoku):
    """
    Operation to update the GUI to the state given as a parameter.
    @param sudoku:  The sudoku states to change the GUI to
    @type sudoku:   Sudoku
    """
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            try:
                SUDOKU[i][j].current(sudoku.get_box(i, j).get_value())
            except tk.TclError:
                SUDOKU[i][j].current(0)


def validate_inputs() -> bool:
    """
    Operation to check if all user inputs are integers ranging from 1 to 9.

    If an input is invalid, a pop up alert is shown detailing the coordinates
    of the incorrect value.
    @return:    True = all inputs are valid, False = an incorrect input has
                been detected
    @rtype:     bool
    """
    x = ""
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            try:
                x = SUDOKU[i][j].get()
                if x != "" and (int(x) < 1 or int(x) > 9):
                    raise ValueError
            except ValueError:
                messagebox.showerror(title="Error",
                                     message="The value at coordinate (" + str(
                                         i) + ", " + str(
                                         j) + ") is not an integer between 1 and 9. It is '" + str(
                                         x) + "'.")
                return False
    return True


def solve():
    """
    Operation to attempt to solve the sudoku puzzle that the GUI represents.

    If there are any error within the sudoku or the puzzle cannot be solved an
    alert pops up, otherwise the GUI is updated with the solved sudoku puzzle.
    """
    # Converts GUI puzzle to Sudoku instance
    if validate_inputs():
        sudoku = Sudoku(SUDOKU)
        if sudoku.is_valid():
            if sudoku.solve():
                update_gui(sudoku)
            else:
                messagebox.showerror(title="Error", message="Cannot solve.")
                update_gui(sudoku)
        else:
            messagebox.showerror(title="Error",
                                 message="This sudoku is invalid.")


def clear():
    """
    Operation to clear the GUI sudoku puzzle of all it's current values.

    A blank sudoku puzzle remains.
    """
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            SUDOKU[i][j].current(0)


def load_gui():
    """
    Operation to set up and run the tkinter GUI.
    """
    height = 538
    width = 441
    global WINDOW
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("grey_cell.TCombobox", background="grey", relief="flat")
    style.configure("white_cell.TCombobox", background="white", relief="flat")
    WINDOW.geometry("%sx%s" % (width, height))
    WINDOW.resizable(False, False)
    WINDOW.title("Soduko Solver")
    global SUDOKU
    for i in range(0, 9, 1):
        for j in range(0, 9, 1):
            # Creates input box with coordinates (i, j)
            SUDOKU[i].append(
                ttk.Combobox(WINDOW, values=("", 1, 2, 3, 4, 5,
                                             6, 7, 8, 9),
                             width=1, justify="center",
                             font="Verdana 30 bold",
                             height=10, style="grey_cell.TCombobox"))
            SUDOKU[i][j].grid(column=i + 2 * (i // 3), row=j + 2 * (j // 3))
            # Styling
            if ((2 < i < 6) and ((j < 3) or (j > 5))) or (
                    (2 < j < 6) and ((i < 3) or (i > 5))):
                SUDOKU[i][j]['style'] = "white_cell.TCombobox"
    # Adds 3x3 square separators for easier viewing
    i = 3
    while i < 10:
        ttk.Separator(WINDOW, orient=tk.VERTICAL).grid(column=i, row=0,
                                                       rowspan=13,
                                                       sticky='ns')
        ttk.Separator(WINDOW, orient=tk.HORIZONTAL).grid(column=0, row=i,
                                                         columnspan=13,
                                                         sticky='we')
        i += 1
        if i == 5:
            i = 8

    tk.Button(WINDOW, text="Solve",
              font="Verdana 16 bold", command=solve, background="grey",
              foreground="white").grid(column=7, row=14,
                                       columnspan=7,
                                       sticky="we")
    tk.Button(WINDOW, text="Clear",
              font="Verdana 16 bold", command=clear).grid(column=0, row=14,
                                                          columnspan=6,
                                                          sticky="we")
    WINDOW.mainloop()


def main():
    """
    Function to run if this script is executed - loads the Sudoku Solver GUI.
    """
    load_gui()


if __name__ == "__main__":
    main()
