class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)



class Ship_Settings:
    
    def __init__(self):
        """Initialize the ship static settings."""

        # Ship settings
        # self.ship_vertical_speed = 0.15
        # self.ship_horizontal_speed = 1.0
        self.ship_limit = 1

        self.initialize_ship_dynamic_settings()

        # How quickly the ship speeds up
        self.ship_speedup_scale = 1.1

    def initialize_ship_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_vertical_speed = 0.15
        self.ship_horizontal_speed = 1.0

    def increase_ship_speed(self):
        """Increase speed settings."""
        self.ship_vertical_speed *= self.ship_speedup_scale
        self.ship_horizontal_speed *= self.ship_speedup_scale

class Bullets_Settings:

    def __init__(self):
        """Initialize the bullet's static settings."""

        # Bullet settings
        # self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 10

        # Big Bullet settings
        # self.big_bullet_speed = 0.4
        self.big_bullet_width = 30000000
        self.big_bullet_height = 30
        self.big_bullet_color = (0, 255, 0)
        self.big_bullets_allowed = 2

        self.initialize_bullets_dynamic_settings()

        # How quickly the bullets speeds up
        self.bullet_speedup_scale = 1.1

    def initialize_bullets_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.bullet_speed = 1.0
        self.big_bullet_speed = 0.4

    def increase_bullet_speed(self):
        """Increase speed settings."""
        self.bullet_speed *= self.bullet_speedup_scale
        self.big_bullet_speed *= self.bullet_speedup_scale
        

class Aliens_Settings:

    def __init__(self):
        """Initialize the aliens's static settings."""

        self.fleet_drop_speed = 10
        self.initialize_aliens_dynamic_settings()

        # How quickly the aliens speeds up
        self.aliens_speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

    def initialize_aliens_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.alien_speed = 0.25

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_point = 50

    def increase_alien_speed(self):
        """Increase speed settings and alien point values."""
        self.alien_speed *= self.aliens_speedup_scale

        self.alien_points = int(self.alien_point * self.score_scale)



