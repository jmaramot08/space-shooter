import pygame

class Ship:
    """A class to manage the ship."""

    # ai_game argument will give Ship access to all the game resources defined
    # in AlienInvasion
    def __init__(self, ai_game):
        """Initialize the ship and set its starting point."""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's vertical position.
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's y value, not the rect.
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom - 50:
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top > 50:
            self.y -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)