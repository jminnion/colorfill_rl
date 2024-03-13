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
        # TODO - helper function to grab an observation using the Board.to_numpy_matrix() and
        #   (yet to be written) Blob.to_numpy_matrix() functions? Will Board be stored somewhere?
        obs = {
            "board": self._board.to_numpy_matrix(),
            "blob": None
        }
        
        return obs
    
    def _get_info(self):
        return {}

    def reset(self, 
              seed: int|None = None,
              options: dict[str, Any]|None = None
              ) -> tuple:    # TODO - define tuple element types
        # seeds self.np_random
        super().reset(seed=seed)

        # initiate a new episode
        #   make a new Board
        self._board: cf.Board = cf.Board(rand_generator=self.np_random)



        observation = None
        info = None

        # TODO - render for "human" render_mode

        return observation, info
    
    def step(self, 
             action) -> tuple:    # TODO - define `action` type and tuple element types
        # TODO - take a given action (move) and compute new board
        pass

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        
    def _render_frame(self):
        pass

    def close(self):
        pass
    