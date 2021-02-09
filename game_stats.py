import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # High score
        self.high_score = self.all_time_high()


    # stats that need to reset each time a player starts a new game go here
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        # self.total_aliens_hit = 0
        # self.aliens_hit = 0
        self.score = 0
        self.level = 1

    def all_time_high(self):
        filename = 'all_time_high.json'

        with open(filename) as f:
            all_time_high = json.load(f)
            return all_time_high