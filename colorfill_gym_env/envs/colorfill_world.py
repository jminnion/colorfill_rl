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


### CLASS DEFINITIONS ###
class ColorfillWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, 
                 render_mode: str|None = None, 
                 size: int = 14):
        self.size = size
        self.window_size = 560      # =14*40, for 40px per Tile

        # TODO - self.observation_space
        # TODO - self.action_space

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def reset(self, 
              seed: int|None = None,
              options: dict[str, Any]|None = None) -> tuple:    # TODO - define tuple element types
        # seeds self.np_random
        super().reset(seed=seed)

        # TODO - initiate a new episode
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
    