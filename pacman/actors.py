

from .sprites import char_sprites, pygame
import numpy as np
from .maze import *

DIRECTION_NORMS = [np.array([1, 0]), np.array(
    [-1, 0]), np.array([0, -1]), np.array([0, 1])]


class Pacman():
    def __init__(self, maze, speed=1, scale=2):
        self.maze = maze
        sun = pygame.transform.scale(char_sprites.subsurface(
            pygame.Rect(37, 1, 13, 13)), (13*scale, 13*scale))
        self.sprites = [[sun], [sun], [sun], [sun]]
        for j in range(4):
            for i in range(2):
                sprite = pygame.transform.scale(char_sprites.subsurface(
                    pygame.Rect(5+i*16, 1+j*16, 13, 13)), (13*scale, 13*scale))
                for _ in range(3):
                    self.sprites[j].append(sprite)
        print(self.sprites)
        self.sprite_turn = 0
        self.center = np.array([116*scale, 164*scale])
        self.speed = speed
        self.dir_i = 0
        self.velocity = DIRECTION_NORMS[self.dir_i]*self.speed
        self.scale = scale
        self.size = 13*scale, 13*scale

    def grid_pos(self):
        return self.center//self.maze.tile_size

    def current_tile_i(self):
        x, y = self.grid_pos()  
        return y*28+x

    def next_tile_i(self, current_tile_i):
        nx, ny = DIRECTION_NORMS[self.dir_i]
        return current_tile_i+nx+ny*28

    def current_abstract(self): #abstract is an integer value representing the attribute and the state of the tile
        return self.maze[self.current_tile_i()]

    def current_rect(self):     #return the current rectangle this pacman is on
        return self.maze.grid[self.current_tile_i()]

    def next_abstract(self):
        current_tile_i = self.current_tile_i()
        next_tile_i = self.next_tile_i(current_tile_i)
        return self.maze[next_tile_i]
    
    def next_rect(self):
        current_tile_i = self.current_tile_i()
        next_tile_i = self.next_tile_i(current_tile_i)
        return self.maze.grid[next_tile_i]

    def precise(self):
        return (self.center == self.current_rect().center).all()

    def at_intersection(self):
        abstract = self.current_abstract()
        return (abstract in INTERSECTION and self.precise())

    def turn(self, new_dir: int):
        self.dir_i = new_dir
        self.velocity = DIRECTION_NORMS[self.dir_i]*self.speed

    def eat(self, current_tile_i):
        old = self.maze[current_tile_i]
        if old in INTERSECTION:
            self.maze[current_tile_i] = 4
        else:
            self.maze[current_tile_i] = 1

    def displace(self):
        abstract, current_tile_i = self.current_abstract(), self.current_tile_i()
        nabstract, next_tile_i = self.next_abstract(), self.next_tile_i(current_tile_i)
        if abstract in FOOD:
            self.eat(current_tile_i)
        if not nabstract and self.precise():
            self.velocity *= 0
        self.sprite_turn = (self.sprite_turn + 1) % 7
        self.center += self.velocity

    def draw_on(self, surface):
        surface.blit(self.sprites[self.dir_i][self.sprite_turn],
                     self.center-(self.size[0]/2, self.size[1]/2))
