class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_vertical_speed = 0.50
        self.ship_horizontal_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 10

        # Big Bullet settings
        self.big_bullet_speed = 2.0
        self.big_bullet_width = 6
        self.big_bullet_height = 30
        self.big_bullet_color = (0, 255, 0)
        self.big_bullets_allowed = 3