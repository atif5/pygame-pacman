
from . import *
import time

pygame = actors.pygame

class PacmanGame:
   def __init__(self, scale=3):
      self.scale = scale
      self.screen = pygame.display.set_mode((224*self.scale, 288*self.scale))
      self.maze = assets.PacMaze(scale=self.scale)
      self.pacman = actors.Pacman(self.maze, speed=3, scale=self.scale)
      self.blinky = ghosts.PacManGhost(
         self.maze, "Blinky", 2, scale=self.scale)
      self.pinky = ghosts.PacManGhost(
         self.maze, "Pinky", 2, scale=self.scale)
      self.inky = ghosts.PacManGhost(
         self.maze, "Inky", 2, scale=self.scale)
      self.clyde = ghosts.PacManGhost(
         self.maze, "Clyde", 2, scale=self.scale)
      self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
      self.context = (self.maze, self.pacman, self.ghosts)
      self.time = 0
      self.ftimer = 6
      self.mode = ghosts.SCATTER

   def frighten(self):
      self.change_mode(ghosts.FRIGHTENED)
      for ghost in self.ghosts:
         ghost.next_direction = ghost.reverse_direction()

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
      for ghost in self.ghosts:
         ghost.move(self.context)

   def draw(self):
      self.maze.draw_on(self.screen)
      for ghost in self.ghosts:
         ghost.draw_on(self.screen)
      self.pacman.draw_on(self.screen)

   def is_over(self):
      for ghost in self.ghosts:
         if ghost.ct_index == self.pacman.ct_index:
            if self.mode == ghosts.FRIGHTENED:
               print(f"pacman ate {ghost.name}!")
               ghost.center = ghost.icenter
               time.sleep(2)
            else:
               return True
      return False


   def main(self):
      initiated = False
      game_over = False
      clock = pygame.time.Clock()
      while not game_over:
         game_over = self.is_over()
         game_over = True if pygame.QUIT in map(lambda e: e.type, pygame.event.get()) else game_over
         self.handle_input()
         self.step()
         if self.pacman.energized:
            self.frighten()
            self.pacman.energized = False
         self.draw()
         pygame.display.flip()
         seconds_passed = clock.tick(60)/1000
         self.time += seconds_passed
         self.handle_frightening_time(seconds_passed)
         if not initiated:
            if self.time > 6:
               self.change_mode(ghosts.CHASE)
               initiated = True
         

