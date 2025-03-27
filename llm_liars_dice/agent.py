# agent.py
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch # Or import tensorflow as tf

class LLMAgent:
    def __init__(self, player_index, model_name="distilgpt2"):
        self.player_index = player_index
        self.model_name = model_name
        print(f"Loading model {model_name} for Player {player_index}...")
        # Option 1: Using pipeline (simpler for text generation)
        # self.generator = pipeline('text-generation', model=model_name, max_new_tokens=20)

        # Option 2: More control with AutoModel/AutoTokenizer (better for specific prompting)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print(f"Model {model_name} loaded for Player {player_index}.")


    def decide_action(self, game_state):
        my_dice_str = ", ".join(map(str, game_state["my_dice"]))
        dice_counts_str = ", ".join(map(str, game_state["dice_counts"]))
        bid_str = "No bid yet"
        if game_state["current_bid"]:
            bid = game_state["current_bid"]
            bid_str = f"Player {bid['player']} bid {bid['quantity']} x {bid['face']}'s"

        prompt = f"""
        You are Player {self.player_index} in a game of Liar's Dice.
        Your dice: [{my_dice_str}]
        Dice counts per player (0 to {len(game_state['dice_counts'])-1}): [{dice_counts_str}]
        Total dice in play: {game_state['total_dice']}
        Current bid: {bid_str}
        Game history: {game_state['history']}

        It is your turn. What is your action?
        Choose ONE action:

        1. BID quantity face (e.g., BID 3 4 for three 4's) - Must be higher than the current bid.

        2. CHALLENGE the current bid (only if a bid exists).

        Your action: """

        # Option 1 (Pipeline):
        # response = self.generator(prompt)[0]['generated_text']
        # action_text = response[len(prompt):].strip() # Get only the generated part

        # Option 2 (Manual):
        inputs = self.tokenizer(prompt, return_tensors="pt") # pt for PyTorch, tf for TensorFlow
        # Ensure model runs on CPU if no GPU or limited VRAM. Add .to('cuda') if you have a GPU setup.
        outputs = self.model.generate(**inputs, max_new_tokens=15, pad_token_id=self.tokenizer.eos_token_id)
        action_text = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()


        print(f"Player {self.player_index} (LLM) raw output: {action_text}")
        # --- Add code here to PARSE action_text into a valid game action ---
        # e.g., "BID 3 4" -> {'action': 'bid', 'quantity': 3, 'face': 4}
        # e.g., "CHALLENGE" -> {'action': 'challenge'}
        # This parsing can be tricky! Keep it simple first.
        parsed_action = self.parse_action(action_text, game_state)
        return parsed_action

    def parse_action(self, text, game_state):
        text = text.upper().split('\n')[0] # Take first line, uppercase
        if "CHALLENGE" in text and game_state["current_bid"]:
            return {"action": "challenge"}
        elif "BID" in text:
            parts = text.split()
            try:
                # Find BID and expect two numbers after it
                bid_idx = parts.index("BID")
                if len(parts) > bid_idx + 2:
                    quantity = int(parts[bid_idx + 1])
                    face = int(parts[bid_idx + 2])
                    # Add basic validation based on game state if needed
                    return {"action": "bid", "quantity": quantity, "face": face}
            except (ValueError, IndexError):
                pass # Invalid format

        # Fallback: If parsing fails or LLM gives nonsense, maybe make a safe bid or challenge?
        # For now, just indicate failure or make a default move.
        print(f"Player {self.player_index}: Could not parse LLM action '{text}'. Defaulting/Error needed.")
        # Implement a default safe action, e.g., challenge if possible, or make a minimum bid.
        if game_state["current_bid"]:
            return {"action": "challenge"} # Simple default
        else:
            # Default opening bid: one '1' higher than total dice / 6 ? Or just 1 '1'?
            return {"action": "bid", "quantity": 1, "face": 1} # Very basic default


# Example Usage:
# agent0 = LLMAgent(player_index=0, model_name="distilgpt2")
# dummy_state = LiarsDice(4).get_state_for_player(0) # Get a sample state
# action = agent0.decide_action(dummy_state)
# print(f"Player 0 decided: {action}")
