

from .actors import *
from .sprites import pygame, char_sprites
import math

DN = DIRECTION_NORMS

# modes
SCATTER = 0
CHASE = 1
FRIGHTENED = 2
# # #


def triangulate(tile_pos1, tile_pos2):
    x1, y1 = tile_pos1 % 28, tile_pos1//28
    x2, y2 = tile_pos2 % 28, tile_pos2//28
    return math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))


def blinky_target(game_context: tuple):
    maze, pacman, other = game_context
    return pacman.ct_index


def pinky_target(game_context):
    maze, pacman, other = game_context
    return maze_relative(pacman.ct_index, DN[pacman.direction]*4)


def inky_target(game_context):
    maze, pacman, ghosts = game_context
    offset = maze_relative(pacman.ct_index, DN[pacman.direction]*2)
    blinky = ghosts[0]
    vec = (offset % 28-blinky.ct_index % 28)*2, \
        (offset//28-blinky.ct_index//28)*2
    return maze_relative(blinky.ct_index, vec) % 1008


def clyde_target(game_context):
    maze, pacman, ghosts = game_context
    clyde, blinky = ghosts[-1], ghosts[0]
    if triangulate(pacman.ct_index, clyde.ct_index) < 8:
        return clyde.scatter_target
    else:
        return blinky.guide(game_context)


GHOST_DATA = {
    "Blinky": [25, 65, LEFT, LEFT, np.array((112, 116)), blinky_target],
    "Pinky": [2, 81, LEFT, LEFT, np.array((112, 116)), pinky_target],
    "Inky": [979, 97, LEFT, LEFT, np.array((112, 116)), inky_target],
    "Clyde": [952, 113, LEFT, LEFT, np.array((112, 116)), clyde_target]

}


class PacManGhost(Actor):
    # ghosts will be initialized by strings, with their names
    def __init__(self, maze, name: str, speed, scale=2):
        self.name = name
        self.scatter_target, sprite_offset, direction, ndirection, center, self.guide = GHOST_DATA[
            self.name]
        super().__init__(maze, center*maze.scale, speed, direction)
        # sprite init
        self.sprites = list()
        for i in range(8):
            sprite = pygame.transform.scale(char_sprites.subsurface(
                pygame.Rect(5+i*16, sprite_offset, 14, 14)), (14*scale, 14*scale))
            for _ in range(4):
                self.sprites.append(sprite)
        self.sprite_turn = 0
        ###  ###
        self.mode = SCATTER
        self.size = 14*scale, 14*scale
        self.next_direction = ndirection
        self.target = self.scatter_target

    def displace(self, game_context):
        if self.in_pen():
            self.wait()
            return
        if self.handle_tunneling():
            return
        self.center += self.velocity
        if self.at_intersection() or self.at_pen_exit():
            self.turn(self.direction)
        cx, cy = self.grid_pos()
        new = cy*28+cx
        if self.ct_index != new:
            self.ct_index = new
            self.on_next_tile(game_context=game_context)

    def move(self, game_context):
        self.displace(game_context=game_context)
        self.sprite_turn = (self.sprite_turn + 1) % 8

    def look_ahead(self, game_context) -> int:  # returns the next direction
        nt_index = self.nt_index()
        nabstract = self.next_abstract(nt_index)
        if nabstract not in GHOST_INTERSECTION:
            return self.direction

        if self.mode == CHASE:
            self.target = self.guide(game_context)
        elif self.mode == SCATTER:
            self.target = self.scatter_target
        
        return min(self.possible_directions(next=True),
                   key=lambda t: triangulate(maze_relative(nt_index, DN[t]), self.target))

    def draw_on(self, surface):
        surface.blit(self.sprites[self.direction*8+self.sprite_turn],
                     self.center-(self.size[0]/2, self.size[1]/2))

    def on_next_tile(self, game_context):
        self.direction = self.next_direction
        self.next_direction = self.look_ahead(game_context)

    def in_pen(self):
        return self.current_abstract() == 8

    def at_pen_exit(self):
        return self.current_abstract() == 10 and \
            (self.center == (112*self.maze.scale, 116*self.maze.scale)).all() and \
            self.direction == RIGHT

    def wait(self):
        if not self.next_abstract(self.nt_index()):
            self.turn(self.reverse_direction())
        self.center += self.velocity
        cx, cy = self.grid_pos()
        self.ct_index = cy*28+cx
