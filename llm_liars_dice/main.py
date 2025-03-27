# main.py
from game import LiarsDice
from agent import LLMAgent
import time

NUM_PLAYERS = 4 # Start with 2 for faster testing if needed
MODEL_NAME = "distilgpt2" # Or "google/flan-t5-small"

game = LiarsDice(num_players=NUM_PLAYERS)
agents = [LLMAgent(player_index=i, model_name=MODEL_NAME) for i in range(NUM_PLAYERS)]

while not game.game_over:
    current_player_idx = game.current_player_index
    if game.player_dice_counts[current_player_idx] == 0:
         # Skip player if they have no dice
         game.current_player_index = (game.current_player_index + 1) % game.num_players
         continue

    print(f"\n--- Turn for Player {current_player_idx} ---")
    player_state = game.get_state_for_player(current_player_idx)
    print(f"Player {current_player_idx} sees state: {player_state}") # For debugging

    # Get action from the agent
    start_time = time.time()
    action = agents[current_player_idx].decide_action(player_state)
    end_time = time.time()
    print(f"Player {current_player_idx} chose: {action} (took {end_time - start_time:.2f}s)")

    # --- Add code to apply the action to the game ---
    # This needs methods in your LiarsDice class like game.process_action(action)
    # game.process_action(current_player_idx, action) # This method would update the bid, handle challenges, update dice counts, history etc.

    # --- Temporary placeholder for game logic ---
    if action['action'] == 'bid':
        print(f"Player {current_player_idx} bids {action['quantity']} x {action['face']}'s")
        game.current_bid = {'player': current_player_idx, 'quantity': action['quantity'], 'face': action['face']}
        game.history.append(f"P{current_player_idx} BIDS: {action['quantity']}x{action['face']}")
        game.current_player_index = (game.current_player_index + 1) % game.num_players # Naive turn progression
    elif action['action'] == 'challenge':
        print(f"Player {current_player_idx} challenges!")
        game.history.append(f"P{current_player_idx} CHALLENGES")
        # --- Resolve challenge ---
        print("Challenge resolution logic needed here!")
        # --- For now, just start a new round as a placeholder ---
        print("Starting new round (placeholder resolution)...")
        game.roll_all_dice()
    else:
         print("Unknown action, skipping turn.")
         game.current_player_index = (game.current_player_index + 1) % game.num_players


    # Add a small delay if needed, especially if rounds go too fast
    time.sleep(1)

    # Check game over condition (e.g., only one player left with dice)
    if sum(1 for count in game.player_dice_counts if count > 0) <= 1:
        game.game_over = True
        print("Game Over!")

print("--- End of Game ---")