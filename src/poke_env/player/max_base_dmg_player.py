from poke_env.player.player import Player

class MaxBaseDamagePlayer(Player):
    def choose_move(self, battle):
        print(f'[From {__name__}] in choose_move. Opp active mon: {battle.opponent_active_pokemon}\nMy mon: {battle.active_pokemon}')

        # Chooses a move with the highest base power when possible
        if battle.available_moves:
            # Iterating over available moves to find the one with the highest base power
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            # Creating an order for the selected move
            return self.create_order(best_move)
        else:
            # If no attacking move is available, perform a random switch
            # This involves choosing a random move, which could be a switch or another available action
            return self.choose_random_move(battle)
