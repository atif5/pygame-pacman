

from .sprites import char_sprites, pygame
import numpy as np
from .maze_logic import *

DIRECTION_NORMS = [np.array([1, 0]), np.array(
    [-1, 0]), np.array([0, -1]), np.array([0, 1])]


RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3


class Actor:
    def __init__(self, maze, center, speed, initdir_index):
        self.maze = maze
        self.center = center
        self.speed = speed
        # direction index, that is an integer indicating the velocity normals position in the DIRECTION_NORMS list
        self.direction = initdir_index
        ###  ###
        self.velocity = DIRECTION_NORMS[self.direction]*self.speed
        cx, cy = self.grid_pos()
        self.ct_index = cy*28+cx  # current tile index

    def grid_pos(self):
        return self.center//self.maze.tile_size

    def nt_index(self):  # next tile index
        return maze_relative(self.ct_index, DIRECTION_NORMS[self.direction])

    # abstract is an integer value representing the attribute and the state of the tile
    def current_abstract(self) -> int:
        return self.maze[self.ct_index]

    # return the current rectangle
    def current_rect(self) -> pygame.Rect:
        return self.maze.grid[self.ct_index]

    def next_abstract(self, nt_index):
        return self.maze[nt_index]

    def next_rect(self, nt_index):
        return self.maze.grid[nt_index]

    def reverse_direction(self):
        if self.direction < 2:
            return (not self.direction).real
        else:
            if self.direction == UP:
                return DOWN
            else:
                return UP

    def environment(self, next=False) -> list:
        environ = list()
        ri = self.nt_index() if next else self.ct_index
        for direction in DIRECTION_NORMS:
            environ.append(self.maze[maze_relative(ri, direction)])
        return environ

    # returns the indices of possible directions
    def possible_directions(self, next=False) -> list:
        environ = self.environment(next=next)
        reverse = self.reverse_direction()
        possibles = [UP, LEFT, DOWN, RIGHT]
        return list(filter(lambda direction: bool(environ[direction]) and direction != reverse, possibles))

    def precise(self, tolerance=None) -> bool:
        return (self.center == self.current_rect().center).all()

    def at_intersection(self):
        abstract = self.current_abstract()
        return (abstract in INTERSECTION and self.precise())

    def turn(self, new_direction: int):
        self.direction = new_direction
        self.velocity = DIRECTION_NORMS[self.direction]*self.speed

    def displace(self):
        if self.handle_tunneling():
            return
        self.center += self.velocity
        cx, cy = self.grid_pos()
        new = cy*28+cx
        if self.ct_index != new:
            self.ct_index = new
            self.on_next_tile()

    def handle_tunneling(self) -> bool:
        s = self.maze.scale
        y = 140*s
        if (self.center < (-20*s, y+1)).all() and self.direction == LEFT:
            self.center += (248*s, 0)
            return True
        elif (self.center > (244*s, y-1)).all() and self.direction == RIGHT:
            self.center -= (248*s, 0)
            return True

        return False

    def on_next_tile(self):
        pass


class Pacman(Actor):
    def __init__(self, maze, speed=2, scale=2):  # maze is a PacMaze object
        super().__init__(maze, np.array([116*scale, 212*scale]), speed, LEFT)
        # sprite init
        sun = pygame.transform.scale(char_sprites.subsurface(
            pygame.Rect(37, 1, 13, 13)), (13*scale, 13*scale))
        self.sprites = [[sun], [sun], [sun], [sun]]
        self.death_sprites = list()
        for j in range(4):
            for i in range(2):
                sprite = pygame.transform.scale(char_sprites.subsurface(
                    pygame.Rect(5+i*16, 1+j*16, 13, 13)), (13*scale, 13*scale))
                for _ in range(3):
                    self.sprites[j].append(sprite)

        for i in range(11):
            sprite = pygame.transform.scale(char_sprites.subsurface(
                    pygame.Rect(53+i*16, 1, 13, 15)), (13*scale, 15*scale))
            for _ in range(2):
                self.death_sprites.append(sprite)

        ###  ###
        self.sprite_turn = 0
        self.size = np.array((13*scale, 13*scale))
        self.destination_offset = self.size//2
        self.ate = False
        self.ate_ghost = False
        self.energized = False

    def eat(self) -> None:
        old = self.current_abstract()
        if old in INTERSECTION:
            self.maze[self.ct_index] = 4
        else:
            self.maze[self.ct_index] = 1

        self.ate = True
        if old in ENERGIZER:
            self.energized = True

    def move(self) -> None:
        abstract = self.current_abstract()
        nt_index = self.nt_index()
        nabstract = self.next_abstract(nt_index)
        if not nabstract and self.precise() and self.ct_index not in TUNNEL:
            self.velocity *= 0
        else:
            self.sprite_turn = (self.sprite_turn + 1) % 7
        if not self.ate:
            self.displace()
        else:
            self.ate = False
        if abstract in FOOD:
            self.eat()

    def die(self, surface, sprite_turn):
        surface.blit(self.death_sprites[sprite_turn], self.center-self.destination_offset-(0, 2))


    def draw_on(self, surface):
        surface.blit(self.sprites[self.direction][self.sprite_turn],
                     self.center-self.destination_offset)
