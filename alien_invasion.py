import sys
import pygame

def __init__(self):
    """Initialize the game, and create game resourses."""
    pygame.init()

    self.screen = pygame.display.set_mode((1200,800))
    pygame.display.set_caption("Alien Invasion")

def run_game(self):
    """Start the main loop for the game."""
    while True:
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            # Make the mos recently drawn screen visible.
            pygame.display.flip()

if __name__ == '__main__':
    # Make a ame instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()