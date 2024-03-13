#   colorfill.py
#   A module containing all the pieces of the game
#
#   Developed for Python 3.11

# imports from standard library
from typing import Any, Self
import copy

# imports from external libraries
import numpy as np


### CLASS DEFINITIONS ###
class Color:
    """
    The primary characteristic of a Tile object.

    The default color scheme includes six (6) colors:
        Blue, Black, Red, Yellow, Orange, White
    """
    # constants
    N_COLORS: int = 6
    COLOR_RGB = [
        (0, 0, 255),    # blue
        (0, 0, 0),      # black
        (255, 0, 0),    # red
        (255, 255, 0),  # yellow
        (255, 165, 0),  # orange
        (255, 255, 255) # white
    ]

    _COLOR_DICT_INDEX_TO_NAME = {
        0: "Blue",
        1: "Black",
        2: "Red",
        3: "Yellow",
        4: "Orange",
        5: "White",
    }

    _COLOR_DICT_NAME_TO_INDEX = {
        "Blue": 0,
        "Black": 1,
        "Red": 2,
        "Yellow": 3,
        "Orange": 4,
        "White": 5
    }

    _COLOR_DICT_INDEX_TO_SHORT_NAME = {
        0: "B",
        1: "K",
        2: "R",
        3: "Y",
        4: "O",
        5: "W",
    }

    _COLOR_DICT_SHORT_NAME_TO_INDEX = {
        "B": 0,
        "K": 1,
        "R": 2,
        "Y": 3,
        "O": 4,
        "W": 5
    }

    # methods
    def __init__(self, color_index: int) -> Self:
        assert color_index in range(0, self.N_COLORS)
        self._color_index: int = color_index

    def __eq__(self: Self, other: Self) -> bool:
        return self.color_index == other.color_index
    
    def __hash__(self) -> int:
        return self.color_index
    
    def __repr__(self) -> str:
        return f"Color({self.color_name})"
    
    @property
    def color_index(self) -> int:
        return self._color_index
    
    @color_index.setter
    def color_index(self, new_index: int) -> None:
        assert new_index in range(0, self.N_COLORS)
        self._color_index = new_index

    @property
    def color_name(self) -> str:
        return self._COLOR_DICT_INDEX_TO_NAME[self._color_index]
    
    @property
    def color_name_short(self) -> str:
        return self._COLOR_DICT_INDEX_TO_SHORT_NAME[self._color_index]

    @property
    def color_rgb(self) -> tuple[int, int, int]:
        return self.COLOR_RGB[self._color_index]
    
    @classmethod
    def by_name(cls, name: str) -> Self:
        return Color(color_index=cls._COLOR_DICT_NAME_TO_INDEX[name])
    
    @classmethod
    def by_short_name(cls, short_name: str) -> Self:
        return Color(color_index=cls._COLOR_DICT_SHORT_NAME_TO_INDEX[short_name])
    
    @classmethod
    def __class_getitem__(cls, name):
        """
            Returns a Color object based on the color name provided (e.g. "Blue").
            Useful for creating a "move" for Board.make_move(...).

            Usage: 
                a = Color["Blue"]   # `a` will contain a Color object with Blue (color_index=0)
                b = Color['K']      # `b` will contain a Color object with Black (color_index=1)
        """
        try:
            if (len(name) > 1):     # full name, e.g. "Blue"
                color_index = cls._COLOR_DICT_NAME_TO_INDEX[name]
            else:   # short name, e.g. "B"
                color_index = cls._COLOR_DICT_SHORT_NAME_TO_INDEX[name]
            
            return(Color(color_index))
        except:
            raise IndexError(f"!!! Color.__class_getitem__: provided color name '{name}' caused an error.")
    

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
    def __init__(self, row: int, col: int) -> Self:
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
    def __init__(self, color: Color, position: Position) -> Self:
        self._color: Color = color
        self._position: Position = position
    
    def neighbors(self) -> dict[str, Position]:
        return self._position.neighbors()
    
    @property
    def color(self) -> Color:
        return self._color
    
    @color.setter
    def color(self, new_color: Color) -> None:
        self._color = new_color
    
    @property
    def position(self) -> Position:
        return self._position
    
    def __eq__(self: Self, other: Self) -> bool:
        color_match: bool = self._color == other._color
        position_match: bool = self._position == other._position
        return (color_match and position_match)
    
    def __str__(self) -> str:
        """
            Returns string of format: 'Color@(x,y)'
            Example: Red@(0,1)
        """
        return f"{self.color.color_name}@{self.position}"
    
    def __repr__(self) -> str:
        return self.__str__()
    

class Blob:
    """
    The collection of Tiles that have been filled so far.

    Not the 1958 movie, but highly similar.
    """
    # constants

    # methods
    def __init__(self, first_tile: Tile) -> Self:
        self._filled_tiles: list[Tile] = [first_tile]
        self._filled_color: Color = first_tile.color

    @property
    def filled_tiles(self) -> list[Tile]:
        return self._filled_tiles       # was this necessary? probably no but oh well
    
    @property
    def filled_color(self) -> Color:
        return self._filled_color
    
    @filled_color.setter
    def filled_color(self, new_color: Color) -> None:
        self._filled_color = new_color
        self._update_color()    # updates the color of all Tiles in Blob

    @property
    def n_tiles(self) -> int:   # for better readability when determining size of Blob / Steve McQueen's chances
        return len(self)
    
    def append(self, new_tile: Tile) -> None:
        self._filled_tiles.append(new_tile)

    def remove(self, tile_to_remove: Tile) -> None:
        if (tile_to_remove in self._filled_tiles):
            self._filled_tiles.remove(tile_to_remove)

    def deepcopy(self) -> Self:
        """
            Makes a complete, distinct copy of this Blob.

            But why? When making a move, we compare an old Blob to a new Blob. 
            Python tries to optimize by double-dipping on Tile objects, which prevents that 
            comparison from being successful.

            A less memory-intense approach would be a good continuous improvement here.
        """
        return copy.deepcopy(self)

    def _update_color(self) -> None:
        """
        Private method called when self.filled_color property is updated.
        Updates the Color of all Tiles in Blob.
        """
        for this_tile in self._filled_tiles:
            this_tile.color = self._filled_color

    def __iter__(self) -> list[Tile]:
        return iter(self._filled_tiles)
    
    def __len__(self) -> int:
        return len(self._filled_tiles)
    
    def __getitem__(self, index: int) -> Tile:
        """
            Grabs the Tile at given numeric index. 
            Allows use of subscript.

            TODO: explore if this should be a subclass "BlobQueue"
        """
        return self._filled_tiles[index]
    

class Board:
    """
    A representation of the game board. Contains Tiles and one Blob.
    """
    # constants
    N_ROWS: int = 14
    N_COLS: int = 14
    SEED: int = 27      # for Weird Al fans, incl. me

    # methods
    def __init__(self, 
                 tiles: list[list[Tile]] = None,
                 rows: int = N_ROWS,
                 cols: int = N_COLS, 
                 seed: int = SEED,
                 rand_generator: np.random.Generator|None = None) -> Self:
        self.tiles: list[list[Tile]] = tiles  # BYO tiles
        self.rows: int = rows
        self.cols: int = cols
        
        if (tiles is None and rand_generator is None):
            self.tiles = Board.make_random_board(rows, cols, seed)  # if you left your tiles at home
        elif (tiles is None and rand_generator is not None):
            self.tiles = Board.make_random_board(rand_generator=rand_generator)

        # start the blob (in Chester County, PA)
        self.blob: Blob = Blob(self.tiles[0][0])

        # make the zeroth move to check for adjacent Tiles of the same color as the first
        self.init_blob()

    def __getitem__(self, key: tuple[int, int]) -> Tile | None:
        """Allows subscripting to grab Tile objects.
            Ex: a_board[0,1] --> provides the Tile in row zero, column one."""
        this_tile = None
        try:
            this_tile = self.tiles[key[0]][key[1]]
        except:
            raise TypeError(
                f"""Board.__getitem__: couldn't process provided key: {key}
                    Note key must be a 2-tuple of integers within range [0,13].
                    Example: board[5,5] --> this would provide key=(5,5)."""
                )
        return this_tile

    def init_blob(self) -> None:
        # if the first tile is already touching other tiles of the same color,
        #   expand the initial Blob to include those tiles.
        first_tile_color: Color = self.blob[0].color
        self.make_move(first_tile_color)

    def test_move(self) -> Any:
        """
            Returns a new Board object as if a move was made, but doesn't actually apply the move to this Board.
            Might be useful, not sure yet.
        """
        pass # TODO

    def make_move(self, move_color: Color) -> None:
        """
            Applies a move to the Board, using the given `move_color`.

            Approach / Steps:
                (1) make a duplicate current Blob as the "new" Blob so we can make modifications to it
                (2) make a second duplicate Blob but treat it as a queue of "Tiles yet to check"
                (3) iterate over "Tiles yet to check" queue
                    (a) for each Tile in queue, get a list of its neighbors
                    (b) iterate over neighbors, checking conditions:
                        (1) if neighbor is not a valid position, skip it and stop checking
                        (2) if neighbor is not `move_color`, skip it and stop checking
                        (3) if neighbor is already in "new" blob, skip it and stop checking
                        (4) if neighbor passed the prior 3 checks, add it to the "new" blob, 
                            and also check if this neighbor is in the queue (add to queue if not already there).
                            This step is how we continue exploring for adjacent tiles.
                    (c) having checked all of a Tile's neighbors, deque the Tile
                (4) when queue is empty, we've checked all Blob neighbors (and their neighbors)
                (5) change the color of all Tiles in the "new" Blob to `move_color`
                (6) overwrite the old Blob with "new" Blob
            
            Notes:
                - Step (1) might be avoidable, to be explored someday.
                - I'd love to explore better path-finding algos here, this one is homegrown and likely inefficient.
        """
        # steps (1) and (2)
        new_blob: Blob = self.blob.deepcopy()
        tiles_to_check: Blob = self.blob.deepcopy()

        # step (3)
        while tiles_to_check.n_tiles > 0:
            this_tile_to_check: Tile = tiles_to_check[0]

            # step (3)(a)
            neighbors: list[Position] = this_tile_to_check.neighbors().values()

            # step (3)(b)
            this_neighbor_position: Position
            for this_neighbor_position in neighbors:
                # step (3)(b)(1)
                if self.is_valid_position(this_neighbor_position):
                    this_neighbor_tile: Tile = self.tile_at_position(this_neighbor_position)

                    # step (3)(b)(2)
                    if (this_neighbor_tile.color == move_color):
                        # step (3)(b)(3)
                        if (this_neighbor_tile in new_blob):
                            pass
                        else:
                            # step (3)(b)(4)
                            new_blob.append(this_neighbor_tile)

                            if (this_neighbor_tile in tiles_to_check):
                                pass
                            else:
                                tiles_to_check.append(this_neighbor_tile)
            
            # step (3)(b)(c)
            tiles_to_check.remove(this_tile_to_check)

        # step (5), and step (4) that we've exited the `while` loop
        new_blob.filled_color = move_color
        
        # step (6)
        self.update_blob(new_blob)

    def is_valid_position(self, position: Position) -> bool:
        row_is_valid: bool = (position.row >= 0 and position.row < self.N_ROWS)
        col_is_valid: bool = (position.col >= 0 and position.col < self.N_COLS)
        return (row_is_valid and col_is_valid)

    def tile_at_position(self, position: Position) -> Tile:
        return self.tiles[position.row][position.col]
    
    def update_blob(self, new_blob: Blob) -> None:
        # overwrite the old blob
        self.blob = new_blob

        # update the Color of the Board's Tile objects
        this_tile: Tile
        for this_tile in new_blob:
            self.update_tile_color(position=this_tile.position, new_color=new_blob.filled_color)

    def update_tile_color(self, position: Position, new_color: Color) -> None:
        self.tile_at_position(position).color = new_color

    def possible_moves(self) -> list[Color]:
        """Returns a list of possible moves (as a list of Colors) on the Board with respect to its current Blob."""
        possible_moves: list[Color] = []
        blob_color: Color = self.blob.filled_color

        tile: Tile
        for tile in self.blob:
            neighbors: dict[str, Position] = tile.neighbors()

            neighbor_position: Position
            for neighbor_position in neighbors.values():
                if (self.is_valid_position(neighbor_position)):
                    neighbor_tile: Tile = self.tile_at_position(neighbor_position)
                    neighbor_color: Color = neighbor_tile.color

                    if (neighbor_color != blob_color):
                        if (neighbor_color not in possible_moves):
                            possible_moves.append(neighbor_color)
                
                if (len(possible_moves) == 5):
                    break
            if (len(possible_moves) == 5):
                break
        
        return possible_moves


    @staticmethod
    def make_random_board(rows: int = N_ROWS, 
                          cols: int = N_COLS, 
                          seed: int = SEED,
                          rand_generator: np.random.Generator|None = None
                          ) -> list[list[Tile]]:
        # generate board as numpy ndarray
        if (rand_generator is None):
            np.random.seed(seed=seed)
            board_matrix: np.ndarray = np.random.randint(low=0, high=Color.N_COLORS, size=(rows, cols))
        else:
            # if RNG provided, assume already seeded
            board_matrix: np.ndarray = rand_generator.integers(low=0, high=Color.N_COLORS, size=(rows, cols))

        # convert type and return
        return Board.from_numpy_matrix(board_matrix)
    
    @staticmethod
    def from_numpy_matrix(board_matrix: np.ndarray) -> list[list[Tile]]:
        # quick error checks
        assert board_matrix.shape[0] == Board.N_ROWS
        assert board_matrix.shape[1] == Board.N_COLS

        # make an empty board as python 2D list
        board_tile_list: list[list[Tile|None]] = [[None for _ in range(Board.N_COLS)] for _ in range(Board.N_ROWS)]

        # convert numpy elements (integers at a position) to Tiles
        for i in range(board_matrix.shape[0]):
            for j in range(board_matrix.shape[1]):
                # make the Tile
                new_position = Position(row=i, col=j)
                new_color = Color(color_index=board_matrix[i, j])
                new_tile = Tile(color=new_color, position=new_position)

                # place the Tile
                board_tile_list[i][j] = new_tile
        
        return board_tile_list

    def to_numpy_matrix(self) -> np.ndarray:
        """Convert this Board into a numpy matrix of color indices.
            Used as a lightweight means of transferring this Board's state.
            Useful for plotting / generating image of the Board."""
        board_matrix = np.full(shape=(self.N_ROWS, self.N_COLS), fill_value=-1)

        for i in range(self.N_ROWS):
            for j in range(self.N_COLS):
                board_matrix[i,j] = self.tiles[i][j].color.color_index
        
        return board_matrix
    
    def blob_as_numpy_matrix(self) -> np.ndarray:
        blob_matrix = np.full(shape=(self.rows, self.cols), fill_value=0)

        tile: Tile
        for tile in self.blob:
            x, y = tile.position.row, tile.position.col
            blob_matrix[x,y] = 1
