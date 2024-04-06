#   colorfill_world.py
#   A module for a custom Gymnasium environment for Colorfill boards.
#
#   Based on tutorial provided by Gymnasium: https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/
#
#   Developed for Python 3.11

# imports from standard library
from typing import Any

# imports from external libraries
import gymnasium as gym
import numpy as np
import pygame

from gymnasium import spaces

# import from within package
import colorfill_gym_env.envs.colorfill as cf


### CLASS DEFINITIONS ###
class ColorfillWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, 
                 render_mode: str|None = None, 
                 size: int = 14):
        self.size = size
        self.window_size_height = 700
        self.window_size_width = 600

        # observation space
        """
          Need to explore this more but for now the observation space can be a Dict
          containing the Board (as a Box space) and the Board's Blob (as a Box space).
            - The Board will be a 14x14 grid containing integers [0,5] representing the
              six possible colors.
            - The Blob will be a 14x14 grid containing integers [0,1] representing the
              flooded area of the Board (1=filled, 0=not yet filled)
          May want to revisit this later for MultiDiscrete or MultiBinary spaces, or even
          splitting the Board into six MultiBinary spaces for each color?
        """
        self._obs_shape = (self.size, self.size)
        self.observation_space = spaces.Dict(
            {
                "board": spaces.Box(low=0, high=5, shape=self._obs_shape, dtype=int),
                "blob": spaces.Box(low=0, high=1, shape=self._obs_shape, dtype=int),
            }
        )

        # action space
        #   There are six colors available, though you realistically can choose from a max of
        #   five colors at each turn (choosing the same color twice in a row is silly).
        self.action_space = spaces.Discrete(n=6)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

        # make placeholder definitions for some more instance variables
        self._board: cf.Board = None
        self._score: int = None
        self._moves: list[int] = None

    def _get_obs(self):
        obs = {
            "board": self._board.to_numpy_matrix(),
            "blob": self._board.blob_as_numpy_matrix(),
        }
        
        return obs
    
    def _get_info(self):
        num_tiles_total: int = self.size**2     # =14*14=196
        num_tiles_filled: int = self._board.blob.n_tiles
        is_board_filled: bool = (num_tiles_filled == num_tiles_total)
        num_moves_made: int = len(self._moves)

        return {
            "num_tiles_total": num_tiles_total,
            "num_tiles_filled": num_tiles_filled,
            "is_board_filled": is_board_filled,
            "num_moves_made": num_moves_made
        }

    def reset(self, 
              seed: int|None = None,
              options: dict[str, Any]|None = None
              ) -> tuple:    # TODO - define tuple element types
        # seeds self.np_random
        super().reset(seed=seed)

        # initiate a new episode
        #   make a new Board
        self._board: cf.Board = cf.Board(rand_generator=self.np_random)
        self._score: int = 0
        self._moves: list[int] = []

        observation = self._get_obs()
        info = self._get_info()

        if (self.render_mode == "human"):
            self._render_frame()

        return observation, info
    
    def step(self, 
             action) -> tuple:    # TODO - define `action` type and tuple element types
        # map action -> color
        action_color = cf.Color(color_index=action)

        # count tiles in the Blob before move
        tile_count_before = self._board.blob.n_tiles

        # apply the move to the board
        self._board.make_move(move_color=action_color)

        # count tiles in the Blob after move
        tile_count_after = self._board.blob.n_tiles
        delta_tiles = tile_count_after - tile_count_before

        # update score      
        info = self._get_info()
        terminated = info["is_board_filled"] or (info["num_moves_made"] > 24)

        self._score += self._score_move(delta_tiles=delta_tiles)
        if (terminated):
            self._score += self._final_move_bonus(turn_number=info["num_moves_made"])

        reward = 1  # TODO - define reward function
        observation = self._get_obs()

        if (self.render_mode == "human"):
            self._render_frame()
        
        return observation, reward, terminated, False, info

    def _score_move(self, delta_tiles: int) -> int:
        if (delta_tiles == 0):
            return 0
        
        per_block_bonus = (delta_tiles - 1) * 100
        move_score = (1000 + per_block_bonus) * delta_tiles

        return move_score
    
    def _final_move_bonus(self, turn_number: int) -> int:
        return 2000 * (turn_number**2) - (100000 * turn_number) + 1300000

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        
    def _render_frame(self):
        # rendering constants
        rgb_black: tuple[int, int, int] = (0, 0, 0)
        rgb_gray: tuple[int, int, int] = (128, 128, 128)
        rgb_white: tuple[int, int, int] = (255, 255, 255)
        dim_tile_px: int = 40    # tile size (height and width) in pixels
        dim_board_px: int = dim_tile_px * self.size

        # setup objects if human mode
        if (self.window is None and self.render_mode == "human"):
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size_width, self.window_size_height)
            )
        
        if (self.clock is None and self.render_mode == "human"):
            self.clock = pygame.time.Clock()

        # render the board as a Surface
        board_surface: pygame.Surface = pygame.Surface((dim_board_px, dim_board_px))

        top, left = 0, 0
        width, height = dim_tile_px, dim_tile_px
        rows, cols = self._board.N_ROWS, self._board.N_COLS

        for i in range(rows):
            for j in range(cols):
                top = i * dim_tile_px
                left = j * dim_tile_px
                tile_color_rgb: tuple[int, int, int] = self._board.tile_at_position(cf.Position(i,j)).color.color_rgb

                pygame.draw.rect(board_surface, tile_color_rgb, pygame.Rect((left, top), (width, height)))

        # render canvas
        canvas = pygame.Surface((self.window_size_width, self.window_size_height))

        margin_board_top: int = 20
        margin_board_left: int = (canvas.get_width() - canvas.get_height()) // 2
        margin_board_bottom: int = margin_board_top
        text_area_top: int = margin_board_top + board_surface.get_height() + margin_board_bottom
        text_area_left: int = margin_board_left
        spacing_text: int = 0

        #   add board to canvas
        canvas.fill(rgb_gray)
        canvas.blit(board_surface, (margin_board_left, margin_board_top))

        #   add game stats to canvas
        font = pygame.font.SysFont('DM Mono Regular', 18, bold=True, italic=False)

        if (len(self._moves) > 0):
            last_move_color_name: str = cf.Color(self._moves[-1]).color_name.upper()
            last_move_color_rgb: tuple[int,int,int] = cf.Color(self._moves[-1]).color_rgb
        else:
            last_move_color_name: str = "N/A"
            last_move_color_rgb: tuple[int,int,int] = rgb_black
        
        text_score = font.render(f"> SCORE: {self._score:,}", True, rgb_black)
        text_n_moves = font.render(f"> N MOVES: {len(self._moves)} / 25", True, rgb_black)
        text_last_move = font.render(f"> LAST MOVE: {last_move_color_name}", True, last_move_color_rgb)

        canvas.blit(text_score, (text_area_left, text_area_top))
        text_area_top += text_score.get_height() + spacing_text
        canvas.blit(text_n_moves, (text_area_left, text_area_top))
        text_area_top += text_n_moves.get_height() + spacing_text
        canvas.blit(text_last_move, (text_area_left, text_area_top))

        # now pick where the canvas goes
        if (self.render_mode == "human"):
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:   # i.e., "rgb_array"
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if (self.window is not None):
            pygame.display.quit()
            pygame.quit()
    