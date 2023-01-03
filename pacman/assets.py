
from .sprites import pygame, empty_maze

class Tile:
    pass


class Intersection:
    pass


class PacMaze:
    def __init__(self, scale=1):
        self.scale = scale
        if scale > 1:
            self.visual = pygame.transform.scale(
                empty_maze, (empty_maze.get_width()*scale, empty_maze.get_height()*scale))
        else:
            self.visual = empty_maze
        self.size = self.visual.get_width(), self.visual.get_height()
        self.grid = []
        for j in range(36):
            for i in range(28):
                self.grid.append(pygame.Rect(
                    i*8*scale, j*8*scale, 8*scale, 8*scale))

    def draw_on(self, surface, grids=False):
        surface.blit(self.visual, (0, 24*self.scale))
        if grids:
            for cell in self.grid:
                pygame.draw.rect(surface, "#ffffff", cell, width=1)
