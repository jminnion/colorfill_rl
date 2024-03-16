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
        self.window_size = 560      # =14*40, for 40px per Tile

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

        # TODO - render for "human" render_mode

        return observation, info
    
    def step(self, 
             action) -> tuple:    # TODO - define `action` type and tuple element types
        # map action -> color
        action_color = cf.Color(color_index=action)

        # count tiles in the Blob before move
        tile_count_before = self._board.blob.n_tiles

        # apply the move to the board
        # TODO - stopped here

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
        pass

    def close(self):
        pass
    