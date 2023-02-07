
from .sprites import pygame, empty_maze, WHITE, BLACK
from .actors import np
from .maze import *


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
        self.food_size = self.scale
        self.energizer_size = 3*self.scale
        self.food_map = [(abstract in FOOD).real for abstract in self]


    def draw_on(self, surface):
        surface.blit(self.visual, (0, 24*self.scale))
        start = 113; end = 951
        for i, tile in enumerate(self.grid[start:end], start):
            #pygame.draw.rect(surface, WHITE, self.grid[i], width=1)
            if self.food_map[i]:
                if self[i] in DOT:
                    pygame.draw.circle(
                        surface, WHITE, tile.center, self.food_size)
                if self[i] in ENERGIZER:
                    pygame.draw.circle(
                        surface, WHITE, tile.center, self.energizer_size)

    def __iter__(self):
        for abstract in self.map:
            yield abstract

    def __getitem__(self, key):
        return self.map[key]

    def __setitem__(self, key, value):
        self.map[key] = value
