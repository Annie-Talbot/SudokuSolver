from sudoku.box import Box


class Sudoku:
    """
    Sudoku object used to simulate a sudoku puzzle with functions to solve.

    Attributes:
        _array (array[Box]):    A 9x9 array with each cell holding a Box
                                object that represents that cells value in the
                                sudoku
        _solved (bool): Represents whether this sudoku object is solved (every
                        cell has been assigned one value)
    """
    _array = []
    _solved = False

    def __init__(self, sudoku_array: []):
        """
        Constructor for an instance of a Sudoku object.

        Defines the initial state of the puzzle with the array given.
        @param sudoku_array:    The array holding all cells values to be
                                transferred to this Sudoku object.
        @type sudoku_array: 2 options:
                                9x9 List[Box] -used for cloning a Sudoku object
                                9x9 List[Combobox] -used for transferring a GUI
                                                    sudoku state with each cell
                                                    being a combobox
                                                    (tkinter.ttk.Combobox) to a
                                                    Sudoku object
        """
        self.set_solved(False)
        self._array = [[], [], [], [], [], [], [], [], []]
        if type(sudoku_array[0][0]) == Box:
            for i in range(0, 9, 1):
                for j in range(0, 9, 1):
                    self._array[i].append(
                        Box(sudoku_array[i][j].get_options().copy(), i, j))
        else:
            for i in range(0, 9, 1):
                for j in range(0, 9, 1):
                    value = sudoku_array[i][j].get()
                    if value == "":
                        self._array[i].append(
                            Box([1, 2, 3, 4, 5, 6, 7, 8, 9], i, j))
                    else:
                        self._array[i].append(Box([int(value)], i, j))

    def get_box(self, x: int, y: int) -> Box:
        """
        Getter for the Box object at the coordinates given.
        @param x:   The x coordinate of the Box wanted
        @type x:    int
        @param y:   The y coordinate of the Box wanted
        @type y:    int
        @return:    The Box in the cell with the coordinates given
        @rtype:     Box
        """
        return self._array[x][y]

    def update_box(self, x: int, y: int) -> bool:
        """
        Operation for updating a box's list of possible values.

        Find the box with the coordinates given and removes all values of
        solved boxes in the same row, column and 3x3 square as this box.
        @param x:   The x coordinate of the box to be updated
        @type x:    int
        @param y:   The y coordinate of the box to be updated
        @type y:    int
        @return:    Whether this box has been changed (it's list of possible
                    values has been reduces)
        @rtype:     bool
        """
        box = self._array[x][y]
        changed = False
        if not box.is_solved():
            # remove from options any solved boxes in the column
            col = self._array[x]
            i = 0
            while i < 9:
                if col[i].is_solved() and i != box.get_y():
                    if box.remove_option(col[i].get_value()):
                        changed = True
                i += 1

            if not box.is_solved():
                # remove from options any solved boxes in the row
                row_num = box.get_y()
                i = 0
                while i < 9:
                    if self.get_box(i,
                                    row_num).is_solved() and i != box.get_x():
                        if box.remove_option(
                                self.get_box(i, row_num).get_value()):
                            changed = True
                    i += 1

                if not box.is_solved():
                    # remove from options any solved boxes in the 3x3 square
                    i = box.get_3x3_x()
                    while i < box.get_3x3_x() + 3:
                        j = box.get_3x3_y()
                        while j < box.get_3x3_y() + 3:
                            if self.get_box(i, j).is_solved() and (
                                    i != box.get_x() and j != box.get_y()):
                                if box.remove_option(
                                        self.get_box(i, j).get_value()):
                                    changed = True
                            j += 1
                        i += 1
        return changed

    def solve(self) -> bool:
        """
        Operation to solve the sudoku puzzle represent by this object's state.

        Iterates through every box and updates their list's of possible values.
        For easy sudoku puzzles:
            This will solve and the function is executed.
        For harder sudoku puzzles:
            The iteration will become stuck because the sudoku puzzle will not
            be changing. This is detected and a box is selected that has the
            lowest number of possible values (for highest probability of
            success). These values are cycled through by creating a clone
            Sudoku object with the value selected as the box's value, and then
            attempting to solve. The clone that returns solved and with no
            errors is the solved sudoku puzzle, so the function is executed.

        IMPORTANT:  To prevent errors, a call to the function is_valid() should
                    be  made before calling solve() as to ensure this sudoku
                    puzzle is solvable.
        """
        changing = True
        self.set_solved(True)
        i = 0
        j = 0
        while True:
            curr_box = self.get_box(i, j)
            # Update box and sudoku variables
            if self.update_box(i, j):
                changing = True
            if not curr_box.is_solved():
                # If any box is not solved the sudoku puzzle is not solved
                self.set_solved(False)
            if curr_box.is_empty():
                # A box has no possible value so an error has occurred
                return False

            # Next box in the soduko
            j += 1
            if j > 8:
                i += 1
                j = 0
            if i > 8:
                i = 0
                # Whole sudoku has been traversed and updated
                if self.is_solved():
                    return True
                if not changing:
                    # Soduko has stopped changing
                    # Find box with least number of options
                    best_box = self.find_fewest_option_box()
                    # Attempt to solve with each value of the box selected
                    for option in best_box.get_options():
                        clone = self.copy()
                        clone.get_box(best_box.get_x(),
                                      best_box.get_y()).set_value(option)
                        if clone.solve():
                            # Clone was successful
                            self._array = clone._array
                            return True
                    # No more possibilities - sudoku is invalid
                    return False
                # Reset states for next iteration
                changing = False
                self.set_solved(True)

    def copy(self) -> 'Sudoku':
        """
        Operation for creating an immutable copy of this Sudoku instance
        @return:    The clone of this Sudoku instance
        @rtype:     Sudoku
        """
        return Sudoku(self._array)

    def find_fewest_option_box(self) -> Box:
        """
        Operation for finding the box with the least amount of possible values.
        @return:    The Box object in the sudoku with the fewest options
        @rtype:     Box
        """
        fewest_options = 10
        best_box = Box
        for i in range(0, 9, 1):
            for j in range(0, 9, 1):
                curr_box = self.get_box(i, j)
                if not curr_box.is_solved() and curr_box.get_size() < fewest_options:
                    best_box = curr_box
                    fewest_options = best_box.get_size()
        return best_box

    def is_valid(self) -> bool:
        """
        Operation for checking this sudoku instance is a valid sudoku puzzle.

        Checks every column, row and 3x3 square in the current sudoku array has
        a maximum of 1 occurrence of each integer between 1 and 9 (inclusive).
        @return:    True = the sudoku is currently valid, False = the sudoku
                    contains a duplicate value.
        @rtype:     bool
        """
        # Check columns are valid
        for row in self._array:
            check_box = Box([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 0)
            for box in row:
                value = box.get_value()
                if value != "" and not check_box.remove_option(int(value)):
                    return False
        # Check rows are valid
        for row in range(0, 9, 1):
            check_box = Box([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 0)
            for col in range(0, 9, 1):
                value = self.get_box(row, col).get_value()
                if value != "" and not check_box.remove_option(int(value)):
                    return False
        # Check 3x3 squares are valid
        for x in range(0, 8, 3):
            for y in range(0, 8, 3):
                check_box = Box([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 0)
                for i in range(x, x + 3, 1):
                    for j in range(y, y + 3, 1):
                        value = self.get_box(i, j).get_value()
                        if value != "" and not check_box.remove_option(
                                int(value)):
                            return False
        return True

    def is_solved(self) -> bool:
        """
        Getter for whether this Sudoku instance is solved.
        @return:    True = solved, False = not solved
        @rtype:     bool
        """
        return self._solved

    def set_solved(self, is_solved: bool):
        """
        Setter for whether this Sudoku instance is solved
        @param is_solved:   Value to set this sudoku to
        @type is_solved:    bool
        """
        self._solved = is_solved
