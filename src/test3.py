import asyncio
from poke_env.ps_client import AccountConfiguration
from poke_env.player.max_damage_player import MaxDamagePlayer
from poke_env.player.nd_greedy_player import NDGreedyPlayer
from poke_env.player.nd2 import NDGreedyPlayer2
from poke_env.player.random_player import RandomPlayer
from poke_env.data.teams import taylor, sydney

from configparser import ConfigParser

config = ConfigParser()
config.read('C:\\Users\\KYRIAKOS\\Documents\\poke-env\\config.ini', encoding = 'utf-8')

async def main():
    # --- Configuration ---
    # We use Gen 9 National Dex as per your example
    BATTLE_FORMAT = "gen9nationaldex"
    N_BATTLES = 100

    print(f"Initializing players for {N_BATTLES} battles...")

    # Player 1: NDGreedyPlayer (The new heuristic player)
    # Uses Scizor team, plays against Gardevoir team
    p1 = MaxDamagePlayer(
        account_configuration = AccountConfiguration(config['PLAYER 1']['USERNAME'],
                                                     config['PLAYER 1']['PASSWORD']),
        save_replays = "C:\\Users\\KYRIAKOS\\Music\\poke-env\\replays\\RS_MDvsNDG2",
        battle_format=BATTLE_FORMAT,
        team=taylor,
        opp_team=sydney,
    )

    p1._foo['salamence']['speed'] = 328
    p1._foo['nidoking']['speed'] = 403 ## scarf
    p1._foo['heatran']['speed'] = 278
    p1._foo['landorustherian']['speed'] = 309
    p1._foo['zapdos']['speed'] = 236
    p1._foo['snorlax']['speed'] = 96
    p1._foo['garchomp']['speed'] = 333
    p1._foo['slowking']['speed'] = 58
    p1._foo['scizor']['speed'] = 166
    p1._foo['darmanitan']['speed'] = 289
    p1._foo['venusaur']['speed'] = 196
    p1._foo['clefable']['speed'] = 156

    p1._foo['salamence']['maxHP'] = 331
    p1._foo['nidoking']['maxHP'] = 303
    p1._foo['heatran']['maxHP'] = 323
    p1._foo['landorustherian']['maxHP'] = 389
    p1._foo['zapdos']['maxHP'] = 384
    p1._foo['snorlax']['maxHP'] = 524
    p1._foo['garchomp']['maxHP'] = 357
    p1._foo['slowking']['maxHP'] = 394
    p1._foo['scizor']['maxHP'] = 344
    p1._foo['darmanitan']['maxHP'] = 351
    p1._foo['venusaur']['maxHP'] = 363
    p1._foo['clefable']['maxHP'] = 394

    p1._foo['salamence']['item'] = 'Choice Specs'
    p1._foo['nidoking']['item'] = 'Choice Scarf'
    p1._foo['landorustherian']['item'] = 'Assault Vest'
    p1._foo['garchomp']['item'] = 'Earth Plate'
    p1._foo['scizor']['item'] = 'Choice Band'
    p1._foo['darmanitan']['item'] = 'Life Orb'
    p1._foo['venusaur']['item'] = 'Assault Vest'

    p1._foo['nidoking']['ability'] = 'Sheer Force'
    p1._foo['heatran']['ability'] = 'Flash Fire'
    p1._foo['snorlax']['ability'] = 'Thick Fat'
    p1._foo['scizor']['ability'] = 'Technician'
    p1._foo['darmanitan']['ability'] = 'Sheer Force'
    p1._foo['venusaur']['ability'] = 'Overgrow'
    p1._foo['clefable']['ability'] = 'Unaware'

    p1._foo['salamence']['moves'] = ['dracometeor', 'airslash', 'dragonpulse', 'fireblast']
    p1._foo['nidoking']['moves'] = ['sludgewave', 'earthpower', 'fireblast', 'icebeam']
    p1._foo['heatran']['moves'] = ['substitute', 'fireblast', 'flashcannon', 'steelbeam']
    p1._foo['landorustherian']['moves'] = ['earthquake', 'superpower', 'stoneedge', 'explosion']
    p1._foo['zapdos']['moves'] = ['thunderbolt', 'voltswitch', 'roost', 'aircutter']
    p1._foo['snorlax']['moves'] = ['bodyslam', 'icepunch', 'protect', 'surf']
    p1._foo['garchomp']['moves'] = ['earthquake', 'stoneedge', 'dragonclaw', 'swordsdance']
    p1._foo['slowking']['moves'] = ['hydropump', 'futuresight', 'slackoff', 'teleport']
    p1._foo['scizor']['moves'] = ['bugbite', 'bulletpunch', 'dualwingbeat', 'knockoff']
    p1._foo['darmanitan']['moves'] = ['flareblitz', 'earthquake', 'superpower', 'rockslide']
    p1._foo['venusaur']['moves'] = ['energyball', 'frenzyplant', 'sludgebomb', 'earthpower']
    p1._foo['clefable']['moves'] = ['moonblast', 'calmmind', 'softboiled', 'thunderwave']

    # Player 2: MaxDamagePlayer (The baseline)
    # Uses Gardevoir team, plays against Scizor team
    p2 = NDGreedyPlayer2(
        account_configuration = AccountConfiguration(config['PLAYER 2']['USERNAME'],
                                                     config['PLAYER 2']['PASSWORD']),
        battle_format=BATTLE_FORMAT,
        team=sydney,
        opp_team=taylor,
    )

    p2._foo['salamence']['speed'] = 328
    p2._foo['nidoking']['speed'] = 403 ## scarf
    p2._foo['heatran']['speed'] = 278
    p2._foo['landorustherian']['speed'] = 309
    p2._foo['zapdos']['speed'] = 236
    p2._foo['snorlax']['speed'] = 96
    p2._foo['garchomp']['speed'] = 333
    p2._foo['slowking']['speed'] = 58
    p2._foo['scizor']['speed'] = 166
    p2._foo['darmanitan']['speed'] = 289
    p2._foo['venusaur']['speed'] = 196
    p2._foo['clefable']['speed'] = 156

    p2._foo['salamence']['maxHP'] = 331
    p2._foo['nidoking']['maxHP'] = 303
    p2._foo['heatran']['maxHP'] = 323
    p2._foo['landorustherian']['maxHP'] = 389
    p2._foo['zapdos']['maxHP'] = 384
    p2._foo['snorlax']['maxHP'] = 524
    p2._foo['garchomp']['maxHP'] = 357
    p2._foo['slowking']['maxHP'] = 394
    p2._foo['scizor']['maxHP'] = 344
    p2._foo['darmanitan']['maxHP'] = 351
    p2._foo['venusaur']['maxHP'] = 363
    p2._foo['clefable']['maxHP'] = 394

    p2._foo['salamence']['item'] = 'Choice Specs'
    p2._foo['nidoking']['item'] = 'Choice Scarf'
    p2._foo['landorustherian']['item'] = 'Assault Vest'
    p2._foo['garchomp']['item'] = 'Earth Plate'
    p2._foo['scizor']['item'] = 'Choice Band'
    p2._foo['darmanitan']['item'] = 'Life Orb'
    p2._foo['venusaur']['item'] = 'Assault Vest'

    p2._foo['nidoking']['ability'] = 'Sheer Force'
    p2._foo['heatran']['ability'] = 'Flash Fire'
    p2._foo['snorlax']['ability'] = 'Thick Fat'
    p2._foo['scizor']['ability'] = 'Technician'
    p2._foo['darmanitan']['ability'] = 'Sheer Force'
    p2._foo['venusaur']['ability'] = 'Overgrow'
    p2._foo['clefable']['ability'] = 'Unaware'

    p2._foo['salamence']['moves'] = ['dracometeor', 'airslash', 'dragonpulse', 'fireblast']
    p2._foo['nidoking']['moves'] = ['sludgewave', 'earthpower', 'fireblast', 'icebeam']
    p2._foo['heatran']['moves'] = ['substitute', 'fireblast', 'flashcannon', 'steelbeam']
    p2._foo['landorustherian']['moves'] = ['earthquake', 'stoneedge', 'stoneedge', 'explosion']
    p2._foo['zapdos']['moves'] = ['thunderbolt', 'voltswitch', 'roost', 'aircutter']
    p2._foo['snorlax']['moves'] = ['bodyslam', 'icepunch', 'protect', 'surf']
    p2._foo['garchomp']['moves'] = ['earthquake', 'stoneedge', 'dragonclaw', 'swordsdance']
    p2._foo['slowking']['moves'] = ['hydropump', 'futuresight', 'slackoff', 'teleport']
    p2._foo['scizor']['moves'] = ['bugbite', 'bulletpunch', 'dualwingbeat', 'knockoff']
    p2._foo['darmanitan']['moves'] = ['flareblitz', 'earthquake', 'superpower', 'rockslide']
    p2._foo['venusaur']['moves'] = ['energyball', 'frenzyplant', 'sludgebomb', 'earthpower']
    p2._foo['clefable']['moves'] = ['moonblast', 'calmmind', 'softboiled', 'thunderwave']

    # --- Execution ---
    print("Starting battles...")
    # This runs the battles in parallel (as much as the client allows)
    await p1.battle_against(p2, n_battles=N_BATTLES)

    # --- Results Analysis ---
    print("\n" + "="*30)
    print("       BATTLE RESULTS       ")
    print("="*30)

    p1_wins = p1.n_won_battles
    p2_wins = p2.n_won_battles
    # Ties are battles that finished but weren't won by either (rare in this setup but possible)
    ties = N_BATTLES - p1_wins - p2_wins

    print("Regular Server")
    print(f"Total Games Played: {N_BATTLES}")
    print(f"{type(p1).__name__} (Taylor) Wins: {p1_wins} ({p1_wins/N_BATTLES*100:.1f}%)")
    print(f"{type(p2).__name__} (Sydney) Wins: {p2_wins} ({p2_wins/N_BATTLES*100:.1f}%)")
    print(f"Ties:                {ties}")
    print("="*30)

if __name__ == "__main__":
    asyncio.run(main())
