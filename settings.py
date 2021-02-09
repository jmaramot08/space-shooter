
class Settings:
    """A lass to sotre all the settings for Alien Killahs."""

    def __init__(self):
        """Initializes the game's static settings."""

        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_speed = 1
        self.ship_limit = 3

        # How quickly the game speeds up
        # self.speedup_scale = 2.0

        # How quickly the alien point values increase
        # self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # Bullet settings.
        self.bullet_speed = 1.5
        self.bullet_width = 20
        self.bullet_height = 5
        self.bullet_color = (217, 0, 0)
        self.bullets_allowed = 5

        # Alien settings.
        self.alien_x_speed = 0.25

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.alien_points = 50
        self.aliens_allowed = 3

    # def increase_speed(self):
    #     """Increase speed settings."""
    #     self.alien_x_speed *= self.speedup_scale

    #     self.alien_points = int(self.alien_points * self.score_scale)
        