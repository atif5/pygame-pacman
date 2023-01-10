

from .sprites import char_sprites, pygame
import numpy as np

DIRECTION_NORMS = [np.array([1, 0]), np.array(
    [-1, 0]), np.array([0, 1]), np.array([0, -1])]


class Pacman():
    def __init__(self, maze, speed=1, scale=2):
        self.maze = maze
        self.sprites = []
        for i in range(2):
            for j in range(4):
                sprite = pygame.transform.scale(char_sprites.subsurface(
                    pygame.Rect(5+i*16, 1+j*16, 13, 13)), (13*scale, 13*scale))
                self.sprites.append(sprite)
        self.sprite_turn = 0
        self.center = np.array([116*scale, 164*scale])
        self.tile = maze[0]
        self.velocity = DIRECTION_NORMS[0]*speed
        self.scale = scale
        self.size = self.sprites[0].get_width(), self.sprites[0].get_height()

    def current_tile(self):
        return self.maze.at(*(self.center//self.maze.tile_size))

    def eat(self, current_tile_i):
        self.maze.map[current_tile_i] = 1

    def displace(self):
        self.center += self.velocity
        current_tile_i = self.maze.grid.index(self.current_tile())
        if self.maze.map[current_tile_i] in [2, 6, 7]:
            self.eat(current_tile_i)
        #self.sprite_turn = (self.sprite_turn + 1) % 3

    def draw_on(self, surface):
        surface.blit(self.sprites[self.sprite_turn],
                     self.center-(self.size[0]/2, self.size[1]/2))
