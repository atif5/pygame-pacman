
from . import *
import time

pygame = actors.pygame


def clear(surface):
    surface.fill(sprites.WHITE)
    surface.fill(sprites.BLACK)


class PacmanGame:
    def __init__(self, scale=2):
        self.scale = scale
        self.screen = pygame.display.set_mode((224*self.scale, 288*self.scale))
        pygame.display.set_caption("Cusman!")
        pygame.display.flip()
        self.maze = assets.PacMaze(scale=self.scale)

        self.pacman = actors.Pacman(self.maze, speed=2, scale=self.scale)

        self.blinky = ghosts.PacManGhost(
            self.maze, "Blinky", 2, scale=self.scale)
        self.pinky = ghosts.PacManGhost(
            self.maze, "Pinky", 2, scale=self.scale)
        self.blinky.icenter = self.pinky.icenter.copy()
        self.inky = ghosts.PacManGhost(
            self.maze, "Inky", 2, scale=self.scale)
        self.clyde = ghosts.PacManGhost(
            self.maze, "Clyde", 2, scale=self.scale)

        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        self.context = (self.maze, self.pacman, self.ghosts)
        self.time = 0
        self.ftimer = 6
        self.mode = ghosts.SCATTER
        self.score = 0
        self.over = False

        self.events = [(2, self.release, self.pinky), (10, self.change_mode, ghosts.CHASE),
                       (15, self.release, self.inky), (21, self.release, self.clyde),
                       (26, self.change_mode, ghosts.SCATTER), (30, self.change_mode, ghosts.CHASE)]

    def handle_events(self):
        for event in self.events:
            t, f, r = event
            if self.time >= t:
                f(r)
                self.events.remove(event)

    def frighten(self):
        self.change_mode(ghosts.FRIGHTENED)
        for ghost in self.ghosts:
            if ghost.in_pen() or ghost.exiting:
                continue
            ghost.next_direction = ghost.reverse_direction()

    def release(self, ghost):
        ghost.exiting = True

    def handle_frightening_time(self, tick):
        if self.mode == ghosts.FRIGHTENED:
            if self.ftimer > 0:
                self.ftimer -= tick
            else:
                self.ftimer = 6
                self.change_mode(ghosts.CHASE)

    def change_mode(self, new_mode):
        print("changing mode to:", new_mode)
        for ghost in self.ghosts:
            ghost.mode = new_mode
        self.mode = new_mode

    def handle_input(self):
        kstate = pygame.key.get_pressed()
        rstates = kstate[pygame.K_RIGHT], kstate[pygame.K_LEFT], kstate[pygame.K_UP], kstate[pygame.K_DOWN]
        if any(rstates):
            i = rstates.index(True)
            if self.pacman.at_intersection() or i == self.pacman.reverse_direction():
                self.pacman.turn(i)

    def step(self):
        self.pacman.move()
        self.handle_collisions()
        for ghost in self.ghosts:
            ghost.move(self.context)
        self.handle_collisions()

    def draw(self, *exclusions):
        self.maze.draw_on(self.screen)
        for ghost in self.ghosts:
            if ghost in exclusions:
                continue
            ghost.draw_on(self.screen)

        if self.pacman in exclusions:
            return
        self.pacman.draw_on(self.screen)

    def handle_collisions(self):
        for ghost in self.ghosts:
            if ghost.ct_index == self.pacman.ct_index:
                if ghost.eaten:
                    continue
                if ghost.mode == ghosts.FRIGHTENED:
                    print(f"pacman ate {ghost.name}!")
                    self.draw(self.pacman, ghost)
                    pygame.display.flip()
                    time.sleep(1.5)
                    ghost.eaten = True
                    ghost.gonna_double = True
                else:
                    self.over = True

    def main(self):
        clock = pygame.time.Clock()
        while not self.over:
            print(self.blinky.velocity)
            self.over = True if pygame.QUIT in map(
                lambda e: e.type, pygame.event.get()) else self.over
            self.handle_input()
            self.step()
            if self.pacman.energized:
                self.frighten()
                self.pacman.energized = False
            self.draw()
            pygame.draw.circle(self.screen, "#00ff00", self.blinky.center, 2)
            pygame.display.flip()
            seconds_passed = clock.tick(60)/1000
            if self.mode != ghosts.FRIGHTENED:
                self.time += seconds_passed
            self.handle_frightening_time(seconds_passed)
            self.handle_events()
