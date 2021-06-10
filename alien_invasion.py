import sys
import pygame
from settings import Settings, Bullets_Settings, Ship_Settings
from ship import Ship
from bullet import Bullet, Big_Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resourses."""
        pygame.init()
        self.settings = Settings()
        self.bullet_settings = Bullets_Settings()
        self.ship_settings = Ship_Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen .get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.big_bullets = pygame.sprite.Group()


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            """Start the main loop for the game."""
            while True:
                self._check_events()
                self.ship.update()
                self._update_bullets()
                self._update_big_bullets()                
                self._update_screen()

                # Make the mos recently drawn screen visible.
                pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)             
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True 
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True 
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_LALT:
            self._fire_big_bullet()

         
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.bullet_settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_big_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.big_bullets) < self.bullet_settings.big_bullets_allowed:
            new_big_bullet = Big_Bullet(self)
            self.big_bullets.add(new_big_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_big_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.big_bullets.update()

        # Get rid of bullets that have disappeared.
        for big_bullet in self.big_bullets.copy():
            if big_bullet.rect.bottom <= 0:
                self.big_bullets.remove(big_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for big_bullet in self.big_bullets.sprites():
            big_bullet.draw_big_bullet()
   

if __name__ == '__main__':
    # Make a ame instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()