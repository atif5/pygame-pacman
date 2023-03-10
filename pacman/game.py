
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
        self.just_eaten = None
        self.context = (self.maze, self.pacman, self.ghosts)
        self.clock = pygame.time.Clock()
        self.time = 0  # global time
        self.ftimer = 6  # frightened timer
        self.ptimer = 1.5  # pause timer
        self.mode = ghosts.SCATTER  # current mode
        self.score = 0
        self.food = 242 # amount of food left
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

    def on_energized(self):
        self.ftimer = 6
        self.change_mode(ghosts.FRIGHTENED)
        for ghost in self.ghosts:
            ghost.blinking = False
            ghost.sprite_turn %= 10
        
        self.pacman.energized = False

    def on_pacman_eating(self):
        if self.pacman.energized:
            self.update_visual()
            self.on_energized()
        else:
            self.update_visual()
            self.food -= 1
            if self.food == 0:
                self.over = True

    def on_ghost_eaten(self, ghost):
        print(f"pacman ate {ghost.name}!")
        self.pacman.ate_ghost = True
        self.just_eaten = ghost
        ghost.eaten = True
        ghost.gonna_double = True

    def release(self, ghost):
        ghost.exiting = True

    def handle_frightening_time(self, tick):
        if self.ftimer < 2:
            for ghost in self.ghosts:
                if ghost.mode == ghosts.FRIGHTENED:
                    ghost.blinking = True
        if self.ftimer > 0:
            self.ftimer -= tick
        else:
            self.ftimer = 6
            for ghost in self.ghosts:
                ghost.blinking = False
            self.change_mode(ghosts.CHASE)

    def change_mode(self, new_mode):
        print("changing mode to:", new_mode)
        for ghost in self.ghosts:
            ghost.mode = new_mode
            if ghost.in_pen() or ghost.exiting or ghost.entering:
                continue
            if not self.mode == ghosts.FRIGHTENED:
                ghost.next_direction = ghost.reverse_direction()

        self.mode = new_mode

    def handle_input(self):
        kstate = pygame.key.get_pressed()
        rstates = kstate[pygame.K_RIGHT], kstate[pygame.K_LEFT], kstate[pygame.K_UP], kstate[pygame.K_DOWN]
        if any(rstates):
            i = rstates.index(True)
            if self.pacman.at_intersection() or i == self.pacman.reverse_direction():
                self.pacman.turn(i)

    def step(self, *exclusions):
        self.handle_collisions()
        for ghost in self.ghosts:
            if ghost in exclusions:
                continue
            ghost.move(self.context)
        
        if self.pacman in exclusions:
            return
        self.pacman.move()
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

    def update_visual(self):
        c = self.maze.grid[self.pacman.ct_index].center
        pygame.draw.circle(self.maze.visual, sprites.BLACK,
                           (c[0], c[1]-24*self.scale), 9)

    def handle_collisions(self):
        for ghost in self.ghosts:
            if ghost.ct_index == self.pacman.ct_index:
                if ghost.eaten:
                    continue
                if ghost.mode == ghosts.FRIGHTENED:
                    self.on_ghost_eaten(ghost)
                else:
                    self.over = True
    
    def handle_time(self, tick):
        if self.mode != ghosts.FRIGHTENED:
            self.time += tick
        else:
            self.handle_frightening_time(tick)

    def handle_pause(self):
        exclusions = [ghost for ghost in self.ghosts if not ghost.eaten or ghost is self.just_eaten]
        self.step(*exclusions, self.pacman)
        self.draw(self.pacman, self.just_eaten)
        pygame.display.flip()
        seconds_passed = self.clock.tick(60)/1000
        self.ptimer -= seconds_passed
        if self.ptimer < 0:
            self.pacman.ate_ghost = False
            self.just_eaten = None
            self.ptimer = 1.5

    def kill_pacman(self):
        for i in range(len(self.pacman.death_sprites)):
            self.draw(*self.ghosts, self.pacman)
            self.pacman.die(self.screen, i)
            pygame.display.flip()
            self.clock.tick(30)
        

    def main(self):
        while not self.over:
            if self.pacman.ate_ghost:
                self.handle_pause()
                continue
            self.over = True if pygame.QUIT in map(
                lambda e: e.type, pygame.event.get()) else self.over
            self.handle_input()
            self.step()
            self.draw(self.just_eaten)
            if self.pacman.ate:
                self.on_pacman_eating()
            pygame.display.flip()
            tick = self.clock.tick(60)/1000
            self.handle_time(tick)
            self.handle_events()

        time.sleep(1)
        self.kill_pacman()
            
