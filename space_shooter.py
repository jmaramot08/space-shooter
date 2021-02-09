# 12-6. Sideways Shooter
# 13-5. Sideways Shooter Part 2
# 13-6. Game Over
# Sideways Shooter, Final Version

import sys
from time import sleep
import json

import pygame

# to access our game settings
from settings import Settings

# to access the ship
from ship import Ship

# to access the bullets
from bullet import Bullet

from alien import Alien

from game_stats import GameStats

from button import Button

from scoreboard import Scoreboard

from random import randint

import random

class SidewaysShooter:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()

        # Set the game window size.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # Set the game windw to fullscreen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        # Set the window title.
        pygame.display.set_caption("Space Shooter")

        # Instance to store game stats.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create instance of a ship.
        # the self argument refers to the current instance of AlienInvasion
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self.play_button = Button(self, "PLAY")

        self._create_aliens()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                # ship movements
                self.ship.update()

                # bullet movements
                self._update_bullets()

                self._check_score()

                # alien movements
                self._update_aliens()

            self._update_screen()


    def _create_aliens(self):
        """Create army of aliens."""
        alien = Alien(self)

        for alien_number in range(self.settings.aliens_allowed):
            self._create_alien(alien_number)


    def _create_alien(self, alien_number):
        """Create a new alien and adds to aliens group."""
        # control the number of aliens created
        
        if len(self.aliens) < self.settings.aliens_allowed:
            new_alien = Alien(self)
            new_alien_width, new_alien_height = new_alien.rect.size

            # How to give each new alien a different speed????
            # speed_factor = [1, 2.0]
            # new_alien.settings.alien_x_speed = random.choice(speed_factor) * self.settings.alien_x_speed
            
            # how to ensure aliens don't spawn on top of each other??
            new_alien.x = 1200 + new_alien_width * alien_number * 2
            new_alien.rect.x = new_alien.x
            new_alien.y = random.randrange(new_alien_height, 800 - 2*new_alien_height, new_alien_height)
            new_alien.rect.y = new_alien.y

                            
            self.aliens.add(new_alien)


    # helper method denoted by _method_name
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._store_high()
                sys.exit()

            # Moving the ship
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
            # Reset game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game stats.
            # hide the mouse cursor
            pygame.mouse.set_visible(False)

            self.stats.reset_stats()
            self.stats.game_active = True

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create aliens and center ship.
            self._create_aliens()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

        # to exit the game by pressing q
        elif event.key == pygame.K_q:
            self._store_high()
            sys.exit()

        # to fire bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _store_high(self):
        """Stores the high score."""
        filename = 'all_time_high.json'
        with open(filename, 'w') as f:
            json.dump(self.stats.high_score, f)


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= 1200:
                self.bullets.remove(bullet)


        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided and resets aliens
        # after all have been shot.

        collisions = pygame.sprite.groupcollide(
                            self.bullets, self.aliens, True, True)

        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
            # print("Collisions: {}".format(len(collisions)))


    def _check_score(self):

        # how to increment game settings automatically when a certain score is reached???

        if self.stats.score >= 1000:
            self.stats.level = 2
            self.settings.aliens_allowed = 4
            self.settings.alien_points = 75
            self.sb.prep_level()

        if self.stats.score >= 2200:
            self.stats.level = 3
            self.settings.aliens_allowed = 5
            self.settings.alien_points = 100
            self.sb.prep_level()

        if self.stats.score >= 4500:
            self.stats.level = 4
            self.settings.aliens_allowed = 6
            self.settings.alien_points = 125
            self.sb.prep_level()

        if self.stats.score >= 8000:
            self.stats.level = 5
            self.settings.aliens_allowed = 7
            self.settings.alien_points = 150
            self.sb.prep_level()

        
    
    def _update_aliens(self):
        "Move aliens left toward ship."
        self.aliens.update()

        # how to make first aliens appear one at a time???
        for alien in self.aliens.sprites():
            if alien.rect.left <= 1000:
                self._create_aliens()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_left()
    

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            self._create_aliens()
            self.ship.center_ship()

            # Pause
            sleep(1.0)

        else:
            self.stats.game_active = False
            self.stats.reset_stats()
            pygame.mouse.set_visible(True)

    
    def _check_aliens_left(self):
        """Check if any aliens have reached the left of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # if alien hits left of screen, treat as if ship was hit
            if alien.rect.left <= screen_rect.left:
                self._ship_hit()
                break


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # Draws ship on the screen.
        self.ship.blitme()

        # Draws the the bullets on the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draws the score information
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

 

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = SidewaysShooter()
    ai.run_game()

