class Box:
    """
    Box object used to represent a single cell in a sudoku game.

    This object holds all values this sudoku cell could take in it's list
    'options', its x and y coordinates within the sudoku board, and provides
    functionality to remove/set these values.

    Attributes:
        _options (array[int]):   The list containing all possible values this
                                cell could take
        _x (int):    The x coordinate of this cell within the sudoku (could
                    range from 0 to 8)
        _y (int):    The y coordinate of this cell within the sudoku (could
                    range from 0 to 8)
        _square_x (int): The x coordinate of the top-left cell of the 3x3 square
                        that this box belongs to
        _square_y (int): The y coordinate of the top-left cell of the 3x3 square
        that this box belongs to
    """
    _options = []
    _x = 0
    _y = 0
    _square_x = 0
    _square_y = 0

    def __init__(self, options: [], x: int, y: int):
        """
        Constructor for an instance of the Box object.

        This defines the values this box could take and its position in the
        sudoku board.

        @param options: A list containing all the possible values this box
                        could take
        @type options:  array[int]
        @param x:   The x coordinate of this box
        @type x:    int
        @param y:   The y coordinate of this box
        @type y:    int
        """
        self._options = options
        self._x = x
        self._y = y
        self._square_x = (x // 3) * 3
        self._square_y = (y // 3) * 3

    def is_solved(self) -> bool:
        """
        Operation to check if this box has been solved.

        If this box only has one possible value to take (in its options) then
        it is solved.
        @return:    True = the box is solved, False = the box is not solved or
                    an error has occurred
        @rtype: bool
        """
        return self.get_size() == 1

    def is_empty(self) -> bool:
        """
        Operation to check if this box has no possible options left.

        If no options are found it means an error has occurred.
        @return: True = no options left, False = 1 or more options left
        @rtype: bool
        """
        return self.get_size() == 0

    def get_x(self) -> int:
        """
        Getter for the x coordinate of this box.
        @return:    The x coordinate of this box
        @rtype:     int
        """
        return self._x

    def get_y(self) -> int:
        """
        Getter for the y coordinate of this box.
        @return:    The y coordinate of this box
        @rtype:     int
        """
        return self._y

    def get_size(self) -> int:
        """
        Getter for the number of possible values this box could take.
        @return:    The number of options
        @rtype:     int
        """
        return len(self._options)

    def remove_option(self, value: int) -> bool:
        """
        Operation for removing a value from the options this box could take.
        @param value:   The value to be removed
        @type value:    int
        @return:    True = options successfully removed, False = the value has
                    already been removed
        @rtype:     bool
        """
        try:
            self._options.remove(int(value))
            return True
        except ValueError:
            return False

    def get_value(self) -> str:
        """
        Getter for the solved value of this box.

        @return:    The value remaining once the box is solved (if unsolved an
                    empty string is returned)
        @rtype:     str
        """
        if self.is_solved():
            return str(self._options[0])
        else:
            return ""

    def set_value(self, value: int):
        """
        Setter for the solved value of this box.
        @param value:   The value to assign to this box (removing all other
                        options)
        @type value:    int
        """
        self._options = [value]

    def get_options(self) -> []:
        """
        Getter for the list of value this box could take
        @return:    The list of values
        @rtype:     List
        """
        return self._options

    def get_3x3_x(self) -> int:
        """
        Getter for the x coordinate of the 3x3 square that this box belongs to.

        @return:    The x coordinate of the top-left cell of the 3x3 square
                    that this box belongs to
        @rtype:     int
        """
        return self._square_x

    def get_3x3_y(self) -> int:
        """
        Getter for the y coordinate of the 3x3 square that this box belongs to.

        @return:    The y coordinate of the top-left cell of the 3x3 square
                    that this box belongs to
        @rtype:     int
        """
        return self._square_y
