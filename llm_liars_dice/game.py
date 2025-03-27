# game.py
import random

class LiarsDice:
    def __init__(self, num_players=4):
        self.num_players = num_players
        self.player_dice_counts = [5] * num_players # Start with 5 dice each
        self.player_hands = [[] for _ in range(num_players)]
        self.current_player_index = 0
        self.current_bid = None # e.g., {'player': index, 'quantity': 2, 'face': 3}
        self.game_over = False
        self.history = [] # Keep track of bids and challenges
        self.roll_all_dice()

    def roll_all_dice(self):
        print("\n--- Rolling dice ---")
        for i in range(self.num_players):
            if self.player_dice_counts[i] > 0:
                self.player_hands[i] = [random.randint(1, 6) for _ in range(self.player_dice_counts[i])]
                print(f"Player {i} rolled: {self.player_hands[i]} (You shouldn't see other's dice in real game)") # For debug
        self.current_player_index = random.randrange(self.num_players) # Random start
        self.current_bid = None
        self.history.append("New round started.")

    def get_total_dice_count(self):
        return sum(self.player_dice_counts)

    # --- Add methods for validation, making bids, challenging, resolving challenges ---
    # --- Add logic for turn progression and player elimination ---

    def get_state_for_player(self, player_index):
        # Information visible to a specific player
        return {
            "my_index": player_index,
            "my_dice": self.player_hands[player_index],
            "dice_counts": self.player_dice_counts.copy(), # How many dice each player has
            "current_bid": self.current_bid,
            "total_dice": self.get_total_dice_count(),
            "current_player_index": self.current_player_index,
            "history": self.history[-5:] # Last 5 events
        }

# Example usage (without LLMs yet)
# game = LiarsDice(4)
# print(game.get_state_for_player(0))