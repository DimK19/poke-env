from poke_env.player.player import Player
import requests
import time

URL_DAMAGE_CALC = "http://localhost:8060/calculate"

class MaxDamagePlayer(Player):
    def _get_damage_calc(
        self,
        spec: str,
        item: str,
        nat: str,
        ab: str,
        evs: dict,
        move: str,
        opp: str,
        opp_item: str,
        opp_nat: str,
        opp_ab: str,
        opp_evs: dict
    ):
        payload = {
            "attacker": {
                "species": spec,
                "item": item,
                "nature": nat,
                "ability": ab,
                "evs": evs
            },
            "defender": {
                "species": opp,
                "item": opp_item,
                "nature": opp_nat,
                "ability": opp_ab,
                "evs": opp_evs
            },
            "move": {
                "name": move
            }
        }

        response = requests.post(URL_DAMAGE_CALC, json = payload).json()

        ## #print(f'payload = {payload}')
        if("damage" in response):
            return response["damage"]
        else:
            return 0

    async def choose_move(self, battle):
        time.sleep(1)
        if(not battle.available_moves):
            # If no attacking move is available, perform a random switch
            # This involves choosing a random move, which could be a switch or another available action
            return self.choose_random_move(battle)

        ## #print(f'[From {__name__}] in choose_move. Opp active mon: {battle.opponent_active_pokemon}\nMy mon: {battle.active_pokemon}')

        ## Get opponent stats
        ## BUG: Sometimes opponent active mon is none
        ###print(f'[From {__name__}] in choose_move. Opp active mon: {battle.active_pokemon}')

        ###print(self._foo)
        opp = battle.opponent_active_pokemon._species.lower()
        opp_item = self._foo[opp]['item']
        opp_nat = self._foo[opp]['nature']
        opp_ab = self._foo[opp]['ability']
        opp_evs = self._foo[opp]['evs']
        ###print(f'opp = {opp} {type(opp)}')

        #print(f'MD {battle.active_pokemon._species} VS {opp}')

        ## Send requests to damage calc middleware to get damage calculations for each move
        options = {}
        for m in battle.available_moves:
            damage = self._get_damage_calc(
                spec = battle.active_pokemon._species,
                item = battle.active_pokemon._item,
                nat = battle.active_pokemon._nature,
                ab = battle.active_pokemon._ability,
                evs = battle.active_pokemon._evs,
                move = m._id,
                opp = opp,
                opp_item = opp_item,
                opp_nat = opp_nat,
                opp_ab = opp_ab,
                opp_evs = opp_evs
            )

            options[m._id] = damage

            #print(f'My {m._id} does {damage}')
        ## Choose max damage
        best_move = max(battle.available_moves, key = lambda m: options[m._id])

        ###print(f'mdp returning move {best_move._id}')
        return self.create_order(best_move)
