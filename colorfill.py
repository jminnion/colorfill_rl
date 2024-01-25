from typing import Any, Self


### CLASS DEFINITIONS ###
class Color:
    """
    The primary characteristic of a Tile object.

    The default color scheme includes six (6) colors:
        Blue, Black, Red, Yellow, Orange, White
    """
    # constants
    N_COLORS: int = 6
    COLOR_LIST: list[int] = list(range(0, N_COLORS))
    COLOR_NAMES: list[str] = ["Blue", "Black", "Red", "Yellow", "Orange", "White"]
    COLOR_NAMES_SHORT: list[str] = ["B", "K", "R", "Y", "O", "W"]
    COLOR_RGB = [
        (0, 0, 255),    # blue
        (0, 0, 0),      # black
        (255, 0, 0),    # red
        (255, 255, 0),  # yellow
        (255, 165, 0),  # orange
        (255, 255, 255) # white
    ]

    # methods
    def __init__(self, color_index: int) -> None:
        assert color_index in self.COLOR_LIST
        self._color_index: int = color_index

    def __eq__(self: Self, other: Self) -> bool:
        return self.color_index == other.color_index
    
    def __hash__(self) -> int:
        return self.color_index
    
    @property
    def color_index(self) -> int:
        return self._color_index
    
    @property.setter
    def color_index(self, new_index) -> None:
        assert new_index in self.COLOR_LIST
        self._color_index = new_index

    @property
    def color_name(self) -> str:
        return self.COLOR_NAMES[self._color_index]
    
    @property
    def color_name_short(self) -> str:
        return self.COLOR_NAMES_SHORT[self._color_index]

    @property
    def color_rgb(self) -> tuple[int, int, int]:
        return self.COLOR_RGB[self._color_index]
    

class Position:
    """
    The location of a Tile object within a Board.

    Conventions:
        - two-element coordinate of format (row, column)
        - (0,0) is top-left, row cooridnates increase rightward 
            and column coordinates increase downward
    """
    # constants

    # methods
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col

    def __eq__(self: Self, other: Self) -> bool:
        return ((self.row == other.row) and (self.col == other.col))
    
    def __hash__(self) -> tuple[int, int]:
        return (self.row, self.col)
    
    def __str__(self) -> str:
        return f"({str(self.row)},{str(self.col)})"
    
    def above(self) -> Self:
        return Position(self.row - 1, self.col)
    
    def below(self) -> Self:
        return Position(self.row + 1, self.col)
    
    def left(self) -> Self:
        return Position(self.row, self.col - 1)
    
    def right(self) -> Self:
        return Position(self.row, self.col + 1)
    
    def neighbors(self) -> dict[str, Self]:
        return {
            "above": self.above(),
            "below": self.below(),
            "left": self.left(),
            "right": self.right()
        }


class Tile:
    """
    A single square on a Board.
    """
    # constants

    # methods
    def __init__(self, color: Color, position: Position) -> None:
        self._color: Color = color
        self._position: Position = position

    def __eq__(self: Self, other: Self) -> bool:
        color_match: bool = self._color == other._color
        position_match: bool = self._position == other._position
        return (color_match and position_match)
    
    def neighbors(self) -> dict[Position]:
        return self._position.neighbors()
    
    @property
    def color(self) -> Color:
        return self._color
    
    @property
    def position(self) -> Position:
        return self._position
    

class Blob:
    """
    The collection of Tiles that have been filled so far.
    """
    # constants

    # methods
    def __init__(self, first_tile: Tile) -> None:
        self._filled_tiles: list[Tile] = [first_tile]
        self._filled_color: Color = first_tile.color

    @property
    def filled_tiles(self) -> list[Tile]:
        return self.filled_tiles
    
    @property
    def filled_color(self) -> Color:
        return self._filled_color
    
    @property.setter
    def filled_color(self, new_color: Color) -> None:
        self._filled_color = new_color

    