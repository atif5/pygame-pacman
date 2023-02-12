

from .actors import *
from .sprites import pygame, char_sprites
import math
import random

DN = DIRECTION_NORMS

# modes
SCATTER = 0
CHASE = 1
FRIGHTENED = 2
# # #

RETARGET = 405


# position of the exit of the monster pen
GATEWAY = np.array((112, 116))


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
    "Pinky": [2, 81, UP, LEFT, np.array((112, 140)), pinky_target],
    "Inky": [979, 97, DOWN, LEFT, np.array((96, 140)), inky_target],
    "Clyde": [952, 113, DOWN, LEFT, np.array((128, 140)), clyde_target]

}


class PacManGhost(Actor):
    # ghosts will be initialized by strings, with their names
    def __init__(self, maze, name: str, speed, scale=2):
        self.name = name
        self.scatter_target, sprite_offset, direction, ndirection, self.icenter, self.guide = GHOST_DATA[
            self.name]
        super().__init__(maze, self.icenter*maze.scale, speed, direction)
        self.icenter *= self.maze.scale
        self.ispeed = self.speed
        # sprite init
        self.sprites = list()
        self.frightened_sprites = list()
        self.eyes = list()
        self.blinking_sprites = list()
        for i in range(8):
            sprite = pygame.transform.scale(char_sprites.subsurface(
                pygame.Rect(5+i*16, sprite_offset, 14, 14)), (14*scale, 14*scale))
            for _ in range(5):
                self.sprites.append(sprite)
        for i in range(2):
            sprite = pygame.transform.scale(char_sprites.subsurface(
                pygame.Rect(133+16*i, 65, 14, 14)), (14*scale, 14*scale))
            for _ in range(5): 
                self.frightened_sprites.append(sprite)
                self.blinking_sprites.append(sprite)
            
        for i in range(2):
            sprite = pygame.transform.scale(char_sprites.subsurface(
                pygame.Rect(165+16*i, 65, 14, 14)), (14*scale, 14*scale))
            for _ in range(10): 
                self.blinking_sprites.append(sprite)
        
        for i in range(4):
            sprite = pygame.transform.scale(char_sprites.subsurface(
                pygame.Rect(133+16*i, 81, 14, 14)), (14*scale, 14*scale))
            self.eyes.append(sprite)

        self.sprite_turn = 0
        ###  ###
        self.mode = SCATTER
        self.size = np.array((14*scale, 14*scale))
        self.destination_offset = self.size//2
        self.next_direction = ndirection
        self.target = self.scatter_target
        self.gateway = GATEWAY*self.maze.scale
        self.eaten = False

        self.exiting = False
        self.entering = False
        self.gonna_double = None
        self.blinking = False

    def displace(self, game_context) -> None:
        if self.handle_special():
            return
        if self.precise() or (self.exiting and self.at_gateway()):
            self.turn(self.direction)
            if self.exiting:
                self.exiting = False
            

        if self.in_tunnel() and not (self.eaten or self.speed == self.ispeed//2):
            self.center += self.velocity//2
        else:
            self.center += self.velocity

        cx, cy = self.grid_pos()
        new = cy*28+cx
        if self.ct_index != new:
            self.ct_index = new
            self.on_next_tile(game_context=game_context)

    def move(self, game_context):
        self.displace(game_context=game_context)
        self.sprite_turn = (self.sprite_turn + 1) % (10 + 20*(self.blinking).real)

    def look_ahead(self, game_context) -> int:  # returns the next direction
        nt_index = self.nt_index()
        nabstract = self.next_abstract(nt_index)
        if nabstract not in INTERSECTION:
            return self.direction

        if self.mode == CHASE:
            self.target = self.guide(game_context)
        elif self.mode == SCATTER:
            self.target = self.scatter_target
        elif self.mode == FRIGHTENED:
            if not self.eaten:
                return random.choice(self.possible_directions(next=True))
        if self.eaten:
            self.target = RETARGET
        possibles = list(self.possible_directions(next=True))
        if nt_index in UP_FORBIDDEN:
            if UP in possibles:
                possibles.remove(UP)

        return min(possibles,
                   key=lambda t: triangulate(maze_relative(nt_index, DN[t]), self.target))

    def on_next_tile(self, game_context):
        self.direction = self.next_direction
        self.next_direction = self.look_ahead(game_context)

    def in_pen(self):
        return self.current_abstract() == 8

    def at_gateway(self):
        return (self.center == self.gateway).all()

    def wait(self):
        nabstract = self.next_abstract(self.nt_index())
        if not nabstract:
            self.turn(self.reverse_direction())
        self.center += self.velocity//2
        cx, cy = self.grid_pos()
        self.ct_index = cy*28+cx

    def enter(self) -> None:
        dx, dy = self.center-self.icenter
        if dy:
            self.direction = DOWN
            self.center += DN[DOWN]
        elif dx:
            self.direction = RIGHT if np.sign(dx) == -1 else LEFT
            self.center += np.sign(dx)*DN[LEFT]
        else: #ghost has finished entering the pen
            self.speed //= 4
            self.eaten = False
            self.entering = False
            self.mode = CHASE
            self.blinking = False
            self.exiting = True #immediately exit after finishing entering

    def exit(self) -> None: #most of the time
        dx, dy = self.center-GATEWAY*self.maze.scale
        if dx:
            self.direction = RIGHT if np.sign(dx) == -1 else LEFT
            self.center += np.sign(dx)*DN[LEFT]
        elif dy:
            self.direction = UP
            self.center += DN[UP]
        else:
            self.direction = LEFT
            return True

    def in_tunnel(self):
        x, y = self.center
        return y == 140*self.maze.scale and (x < 44*self.maze.scale or x > 180*self.maze.scale)

    def handle_special(self) -> bool:
        precise = self.precise()
        if self.eaten:
            if self.at_gateway():
                self.entering = True
                self.ct_index = 0
            elif precise:
                if self.gonna_double:
                    self.speed *= 4
                    self.gonna_double = False
        elif self.mode == FRIGHTENED:
            if self.speed == self.ispeed:
                if precise:
                    self.speed //= 2
        else:
            if precise:
                if self.speed == self.ispeed//2:
                    self.speed *= 2
        if self.entering:
            self.enter()
            return True
        if self.in_pen() and not self.exiting:
            self.wait()
            return True
        if self.handle_tunneling():
            return True
        if self.exiting:
            return not self.exit()
                

    def draw_on(self, surface):
        if self.mode == FRIGHTENED and not self.eaten:
            if self.blinking:
                surface.blit(self.blinking_sprites[self.sprite_turn],
                            self.center-self.destination_offset)
            else:
                surface.blit(self.frightened_sprites[self.sprite_turn],
                         self.center-self.destination_offset)
        elif self.eaten:
            surface.blit(self.eyes[self.direction],
                         self.center-self.destination_offset)

        else:
            surface.blit(self.sprites[10*self.direction+self.sprite_turn],
                         self.center-self.destination_offset)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"PacmanGhost: {self.name}"
