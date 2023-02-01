
from . import *

pygame = actors.pygame


class PacmanGame:
   def __init__(self, scale=3):
      self.scale = scale
      self.screen = pygame.display.set_mode((224*self.scale, 288*self.scale))
      self.maze = assets.PacMaze(scale=self.scale)
      self.pacman = actors.Pacman(self.maze, speed=4, scale=self.scale)
      self.blinky = ghosts.PacManGhost(
         self.maze, "Blinky", 3, scale=self.scale)
      self.pinky = ghosts.PacManGhost(
         self.maze, "Pinky", 3, scale=self.scale)
      self.inky = ghosts.PacManGhost(
         self.maze, "Inky", 3, scale=self.scale)
      self.clyde = ghosts.PacManGhost(
         self.maze, "Clyde", 3, scale=self.scale)
      self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
      self.context = (self.maze, self.pacman, self.ghosts)
      self.time = 0

   def change_mode(self, new_mode):
      for ghost in self.ghosts:
         ghost.mode = new_mode

   def handle_input(self):
      kstate = pygame.key.get_pressed()
      rstates = kstate[pygame.K_RIGHT], kstate[pygame.K_LEFT], kstate[pygame.K_UP], kstate[pygame.K_DOWN]
      if any(rstates):
         i = rstates.index(True)
         if self.pacman.at_intersection() or i == self.pacman.reverse_direction():
            self.pacman.turn(i)

   def step(self):
      self.pacman.move()
      self.clyde.move(self.context)

   def draw(self):
      self.maze.draw_on(self.screen)
      for ghost in self.ghosts:
         ghost.draw_on(self.screen)
      self.pacman.draw_on(self.screen)

   def is_over(self):
      for ghost in self.ghosts:
         if ghost.ct_index == self.pacman.ct_index:
            return True
      return False


   def main(self):
      game_over = False
      clock = pygame.time.Clock()
      while not game_over:
         print(self.time)
         pygame.event.pump()
         self.handle_input()
         game_over = self.is_over()
         self.step()
         self.draw()
         pygame.display.flip()
         self.time += clock.tick(60)/1000
         if self.time > 6:
            self.change_mode(ghosts.CHASE)
