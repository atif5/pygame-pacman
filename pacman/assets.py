
from .sprites import pygame, empty_maze
from .actors import np
from .maze import *


WHITE = "#ffffff"


class PacMaze:
    def __init__(self, scale=2):
        if scale > 1:
            self.visual = pygame.transform.scale(
                empty_maze, (empty_maze.get_width()*scale, empty_maze.get_height()*scale))
        else:
            self.visual = empty_maze
        self.size = self.visual.get_width(), self.visual.get_height()
        self.tile_size = 8*scale
        self.map = MAZE_MAP
        self.grid = []
        for j in range(36):
            for i in range(28):
                temp = pygame.Rect(
                    i*self.tile_size, j*self.tile_size, self.tile_size, self.tile_size)
                self.grid.append(temp)
        self.scale = scale

    def draw_on(self, surface, grids=False):
        surface.blit(self.visual, (0, 24*self.scale))
        if grids:
            for tile in self.grid:
                pygame.draw.rect(surface, WHITE, tile, width=1)
        else:
            for tile in self.grid:
                if self.map[self.grid.index(tile)] in [2, 6]:
                    pygame.draw.circle(
                        surface, WHITE, tile.center, 1*self.scale)
                if self.map[self.grid.index(tile)] in [3, 7]:
                    pygame.draw.circle(
                        surface, WHITE, tile.center, 4*self.scale)

    def __iter__(self):
        for abstract in self.map:
            yield abstract

    def __getitem__(self, key):
        return self.map[key]

    def __setitem__(self, key, value):
        self.map[key] = value
