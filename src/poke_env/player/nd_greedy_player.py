from poke_env.player.player import Player
from poke_env.environment.pokemon import Pokemon
import requests
import math
import random
import time

URL_DAMAGE_CALC = "http://localhost:8060/calculate"

class NDGreedyPlayer(Player):
    """
    Non-Deterministic Greedy Player
    """

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

        ## ##print(f'payload = {payload}')
        if("damage" in response):
            return response["damage"]
        else:
            return 0


    async def play_out_1v1(self, me: Pokemon, opp: Pokemon, my_hp_override = None):
        """
        Play out current 1v1

        At present time assume no speed ties (I have partially implemented
        chess clock speed tie resolution but will not use it)

        Assume max damage move used every turn by each player - obviously this
        is a sub optimal assumption as set up moves can change the outcome

        Find max damage move of me to opp and opp to me
        Calc how many turns each takes to kill the other
        if they are equal the faster wins
        otherwise the lower turn count wins

        current hp implicitly returns number for my mon and % for opp
        the same for max hp
        """

        mekey = me._species.lower().replace('-', '')
        oppkey = opp._species.lower().replace('-', '')

        ####print(f'Playing out {mekey} vs {oppkey}')
        ####print(f'{mekey} max hp {me._max_hp} current hp {me._current_hp}')
        ####print(f'{oppkey} max hp {opp._max_hp} current hp {opp._current_hp}')

        oppobj = {
            'species': oppkey,
            'item': self._foo[oppkey]['item'],
            'nature': self._foo[oppkey]['nature'],
            'ability': self._foo[oppkey]['ability'],
            'evs': self._foo[oppkey]['evs']
        }

        myobj = {
            'species': me._species,
            'item': me._item,
            'nature': me._nature,
            'ability': me._ability,
            'evs': me._evs
        }

        mybm, my_dmg = await self._get_max_damage_move(
            myobj,
            oppobj,
            self._foo[mekey]['moves']
        )

        oppbm, opp_dmg = await self._get_max_damage_move(
            oppobj,
            myobj,
            self._foo[oppkey]['moves']
        )

        myhp = my_hp_override if my_hp_override is not None else me._current_hp
        opphp = int(self._foo[oppkey]['maxHP'] * opp._current_hp / 100)

        ## Turns to kill, turns to die
        ttk = math.ceil(opphp / my_dmg)
        ttd = math.ceil(myhp / opp_dmg)

        ####print(f'Concluded. My best move: {mybm} for {my_dmg}, ttk = {ttk}. Opp {oppbm} for {opp_dmg}, ttd = {ttd}')
        ####print(f'This is because my opponent\'s current hp is {opphp}')

        if(ttk == ttd):
            return self._foo[mekey]['speed'] > self._foo[oppkey]['speed'], ttk
        else:
            return ttk < ttd, min(ttk, ttd)


    async def _get_max_damage_move(self, attacker, defender, moves):
        """
        Finds the move that deals the most damage among the list.
        """

        ####print(f'{__name__} called with att = {attacker}, def = {defender}, moves = {moves}')

        ## Send requests to damage calc middleware to get damage calculations for each move
        options = {}
        for m in moves:
            damage = self._get_damage_calc(
                spec = attacker['species'],
                item = attacker['item'],
                nat = attacker['nature'],
                ab = attacker['ability'],
                evs = attacker['evs'],
                move = m,
                opp = defender['species'],
                opp_item = defender['item'],
                opp_nat = defender['nature'],
                opp_ab = defender['ability'],
                opp_evs = defender['evs']
            )

            options[m] = damage

            ## ##print(f'My {m._id} does {damage}')
        ## Choose max damage
        best_move = max(moves, key = lambda m: options[m])

        return best_move, options[best_move]

    async def choose_move(self, battle):
        time.sleep(1)
        ####print('inside ndgreedy choose move')

        if(not battle or
           not battle.available_moves or
           not battle.opponent_active_pokemon or
           not battle.active_pokemon
        ):
            # If no attacking move is available, perform a random switch
            # This involves choosing a random move, which could be a switch or another available action
            return self.choose_random_move(battle)

        active_mon = battle.active_pokemon
        opp_active = battle.opponent_active_pokemon


        # --- Step 0: Play out current 1v1 ---
        iwin, turns = await self.play_out_1v1(active_mon, opp_active)
        ####print(f'I {"win" if iwin else "lose"}')

        # --- Step 1: Decide to Stay or Switch ---
        should_switch = False

        if battle.available_switches:
            if iwin:
                should_switch = False
            else:
                # Probability formula: max{50, 100 - 10 * turns to lose}
                if random.uniform(0, 100) < max(50, 100 - (10 * turns)):
                    should_switch = True

        # --- Step 2.1: Handle Switching ---
        if should_switch:
            ####print('CALCULATING SWITCH')
            candidates = []
            oppkey = battle.opponent_active_pokemon._species.lower().replace('-', '')
            oppobj = {
                'species': oppkey,
                'item': self._foo[oppkey]['item'],
                'nature': self._foo[oppkey]['nature'],
                'ability': self._foo[oppkey]['ability'],
                'evs': self._foo[oppkey]['evs']
            }

            myobj = {
                'species': battle.active_pokemon._species,
                'item': battle.active_pokemon._item,
                'nature': battle.active_pokemon._nature,
                'ability': battle.active_pokemon._ability,
                'evs': battle.active_pokemon._evs
            }

            oppmove, oppdmg = await self._get_max_damage_move(oppobj,
                                                        myobj,
                                                        self._foo[oppkey]['moves']
                                                        )

            # Evaluate each candidate
            for candidate in battle.available_switches:
                ####print('EXAMINING CANDIDATES')
                # Predict damage candidate takes on switch-in
                # We calculate damage using Opponent (Attacker) -> Candidate (Defender)
                # But using the move selected against the CURRENT pokemon.
                oppkey = battle.opponent_active_pokemon._species.lower().replace('-', '')
                candkey = candidate._species.lower().replace('-', '')
                switch_in_dmg = self._get_damage_calc(
                    spec = oppkey,
                    item = self._foo[oppkey]['item'],
                    nat = self._foo[oppkey]['nature'],
                    ab = self._foo[oppkey]['ability'],
                    evs = self._foo[oppkey]['evs'],
                    move = oppmove,
                    opp = candkey,
                    opp_item = self._foo[candkey]['item'],
                    opp_nat = self._foo[candkey]['nature'],
                    opp_ab = self._foo[candkey]['ability'],
                    opp_evs = self._foo[candkey]['evs']
                )

                ####print(f'Switch in damage = {switch_in_dmg}')

                candidate_hp_after = candidate._current_hp - switch_in_dmg

                if candidate_hp_after <= 0:
                    continue # candidate dies on switch-in

                # Sim 1v1 with candidate (at reduced HP) vs Opponent
                cand_wins, cand_turns = await self.play_out_1v1(candidate, opp_active, my_hp_override=candidate_hp_after)

                if cand_wins:
                    ####print('Found winning cand')
                    candidates.append((candidate, cand_turns))

            # Logic: If all lose, abort (don't switch). If one or more wins, pick fastest.
            if candidates:
                # Sort by turns (ascending)
                best_candidate, _ = min(candidates, key=lambda x: x[1])
                ####print('ndg returning switch')
                return self.create_order(best_candidate)
            else:
                # Abort switch, proceed to Step 2.2
                ##print('NO WINNING CAND FOUND')
                pass

        ##print('after switch')

        # --- Step 2.2: Handle Staying In (Move Selection) ---

        # Determine probability opponent stays in
        opp_team_alive = [p for p in battle.opponent_team.values() if not p.fainted]
        ##print(opp_team_alive)
        if not iwin:
            # If I lose, assume opponent stays to kill me
            p_opp_stay = 1.0
        else:
            # If I win, assume opponent switches 50% of the time (if they have switches)
            # We estimate if they have switches by checking team size vs fainted
            if len(opp_team_alive) > 1:
                p_opp_stay = 0.5
            else:
                p_opp_stay = 1.0

        ##print('!!!!!!!AFTER CALCULATING PROBABILITY OF OPP STAYING IN')

        # Construct Bipartite Graph
        # Left: My Moves, Right: Opponent Team (Active + Bench)
        move_coverage = {m: set() for m in battle.available_moves}

        for opp_mon in opp_team_alive:
            ##print('!!!!!!! LOOPING OVER OPP MONS')
            # Find moves that kill this opp_mon
            killing_moves = []
            max_dmg_val = -1
            max_dmg_moves = []

            for move in battle.available_moves:
                ##print('!!!!!!! CALCING AVAILABLE MOVES')
                oppkey = opp_mon._species.lower().replace('-', '')
                mykey = battle.active_pokemon._species.lower().replace('-', '')
                dmg = self._get_damage_calc(
                    spec = mykey,
                    item = self._foo[mykey]['item'],
                    nat = self._foo[mykey]['nature'],
                    ab = self._foo[mykey]['ability'],
                    evs = self._foo[mykey]['evs'],
                    move = move._id,
                    opp = oppkey,
                    opp_item = self._foo[oppkey]['item'],
                    opp_nat = self._foo[oppkey]['nature'],
                    opp_ab = self._foo[oppkey]['ability'],
                    opp_evs = self._foo[oppkey]['evs']
                )
                opp_hp = opp_mon._current_hp

                if dmg >= opp_hp:
                    killing_moves.append(move)

                # Track max damage for fallback
                if dmg > max_dmg_val:
                    max_dmg_val = dmg
                    max_dmg_moves = [move]
                elif dmg == max_dmg_val:
                    max_dmg_moves.append(move)

            # Edges Round 1: Connect to moves that kill
            if killing_moves:
                for m in killing_moves:
                    move_coverage[m].add(opp_mon.species)
            else:
                # Edges Round 2: Connect to max damage moves
                for m in max_dmg_moves:
                    move_coverage[m].add(opp_mon.species)

        # Decision Time
        if random.random() < p_opp_stay:
            ##print('!!!!!!! DECIDE HE STAYS')
            # Strategy: Click Max Damage vs Current Opponent
            mekey = battle.active_pokemon._species.lower().replace('-', '')
            ##print(mekey)
            oppkey = battle.opponent_active_pokemon._species.lower().replace('-', '')
            ##print(f'mekey = {mekey}, oppkey = {oppkey}')
            oppobj = {
                'species': oppkey,
                'item': self._foo[oppkey]['item'],
                'nature': self._foo[oppkey]['nature'],
                'ability': self._foo[oppkey]['ability'],
                'evs': self._foo[oppkey]['evs']
            }

            myobj = {
                'species': battle.active_pokemon._species,
                'item': battle.active_pokemon._item,
                'nature': battle.active_pokemon._nature,
                'ability': battle.active_pokemon._ability,
                'evs': battle.active_pokemon._evs
            }

            best_move, _ = await self._get_max_damage_move(myobj, oppobj, list(map(lambda x: x._id, battle.available_moves)))
            ##print(f'ndg decided max damage move {best_move}')
            for bm in battle.available_moves:
                if(bm._id == best_move):
                    return self.create_order(bm)
        else:
            ##print('!!!!!!! DECIDE HE SWITCHES')
            # Strategy: Click Move with Highest Degree in Graph
            # Sort moves by degree (number of covered opponents)
            # If degrees are equal, random choice among them

            scored_moves = []
            for m in battle.available_moves:
                degree = len(move_coverage[m])
                scored_moves.append((m, degree))

            # Find max degree
            max_degree = max(scored_moves, key=lambda x: x[1])[1]
            best_candidates = [m for m, deg in scored_moves if deg == max_degree]

            selected_move = random.choice(best_candidates)
            return self.create_order(selected_move)
