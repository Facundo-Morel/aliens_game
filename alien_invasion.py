import sys
from time import sleep
import pygame
from settings import Settings, Bullets_Settings, Ship_Settings, Aliens_Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet, Big_Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resourses."""
        pygame.init()
        self.settings = Settings()
        self.bullet_settings = Bullets_Settings()
        self.ship_settings = Ship_Settings()
        self.aliens_settings = Aliens_Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen .get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.big_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")



    def run_game(self):
            """Start the main loop for the game."""
            while True:
                self._check_events()

                if self.stats.game_active:
                    self.ship.update()
                    self._update_bullets()
                    self._update_big_bullets() 
                    self._update_aliens()     
                             
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.ship_settings.initialize_ship_dynamic_settings()
            self.bullet_settings.initialize_bullets_dynamic_settings()
            self.aliens_settings.initialize_aliens_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship:
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursos.
            pygame.mouse.set_visible(False)

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

        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.aliens_settings.alien_point * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.aliens_settings.increase_alien_speed()
            self.bullet_settings.increase_bullet_speed()
            self.ship_settings.increase_ship_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_big_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.big_bullets.update()

        # Get rid of bullets that have disappeared.
        for big_bullet in self.big_bullets.copy():
            if big_bullet.rect.bottom <= 0:
                self.big_bullets.remove(big_bullet)

        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
                self.big_bullets, self.aliens, False, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.aliens_settings.alien_point * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _update_aliens(self):
        """ Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.aliens_settings.fleet_drop_speed
        self.aliens_settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (2 * alien_height) - ship_height)
        number_rows = available_space_y // (3 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for big_bullet in self.big_bullets.sprites():
            big_bullet.draw_big_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships( )

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break   
   

if __name__ == '__main__':
    # Make a ame instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()