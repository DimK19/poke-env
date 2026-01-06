from poke_env.player.random_player import RandomPlayer
from poke_env.player.max_damage_player import MaxDamagePlayer
from poke_env.player.nd_greedy_player import NDGreedyPlayer
from poke_env.ps_client import ShowdownServerConfiguration, AccountConfiguration
from poke_env.data import GenData
from poke_env.data.teams import taylor, sydney

from configparser import ConfigParser

config = ConfigParser()
config.read('C:\\Users\\KYRIAKOS\\Documents\\poke-env\\config.ini', encoding = 'utf-8')


p1 = MaxDamagePlayer(
    account_configuration = AccountConfiguration(config['PLAYER 1']['USERNAME'],
                                                 config['PLAYER 1']['PASSWORD']),
    save_replays = "C:\\Users\\KYRIAKOS\\Music\\poke-env\\replays",
    battle_format="gen9nationaldex",
    team = taylor,
    opp_team = sydney
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

p1._foo['salamence']['moves'] = ['dracometeor', 'airslash', 'dragonpulse', 'fireblast']
p1._foo['nidoking']['moves'] = ['sludgewave', 'earthpower', 'fireblast', 'icebeam']
p1._foo['heatran']['moves'] = ['substitute', 'fireblast', 'flashcannon', 'steelbeam']
p1._foo['landorustherian']['moves'] = ['earthquake', 'superpower', 'stoneedge', 'explosion']
p1._foo['zapdos']['moves'] = ['thunderbolt', 'voltswitch', 'roost', 'aircutter']
p1._foo['snorlax']['moves'] = ['bodyslam', 'icepunch', 'protect', 'surf']
p1._foo['garchomp']['moves'] = ['earthquake', 'stoneedge', 'dragonclaw', 'swordsdance']
p1._foo['slowking']['moves'] = ['hydropump', 'futuresight', 'slackoff', 'teleport']
p1._foo['scizor']['moves'] = ['bugbite', 'bulletpunch', 'dualwingbeat', 'knockoff']
p1._foo['darmanitan']['moves'] = ['flareblitz', 'earthquake', 'superpower', 'uturn']
p1._foo['venusaur']['moves'] = ['energyball', 'frenzyplant', 'sludgebomb', 'earthpower']
p1._foo['clefable']['moves'] = ['moonblast', 'calmmind', 'softboiled', 'thunderwave']

p2 = NDGreedyPlayer(
    account_configuration = AccountConfiguration(config['PLAYER 2']['USERNAME'],
                                                 config['PLAYER 2']['PASSWORD']),
    battle_format="gen9nationaldex",
    team = sydney,
    opp_team = taylor
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

p2._foo['salamence']['moves'] = ['dracometeor', 'airslash', 'dragonpulse', 'fireblast']
p2._foo['nidoking']['moves'] = ['sludgewave', 'earthpower', 'fireblast', 'icebeam']
p2._foo['heatran']['moves'] = ['substitute', 'fireblast', 'flashcannon', 'steelbeam']
p2._foo['landorustherian']['moves'] = ['earthquake', 'uturn', 'stoneedge', 'explosion']
p2._foo['zapdos']['moves'] = ['thunderbolt', 'voltswitch', 'roost', 'aircutter']
p2._foo['snorlax']['moves'] = ['bodyslam', 'icepunch', 'protect', 'surf']
p2._foo['garchomp']['moves'] = ['earthquake', 'stoneedge', 'dragonclaw', 'swordsdance']
p2._foo['slowking']['moves'] = ['hydropump', 'futuresight', 'slackoff', 'teleport']
p2._foo['scizor']['moves'] = ['bugbite', 'bulletpunch', 'dualwingbeat', 'knockoff']
p2._foo['darmanitan']['moves'] = ['flareblitz', 'earthquake', 'superpower', 'uturn']
p2._foo['venusaur']['moves'] = ['energyball', 'frenzyplant', 'sludgebomb', 'earthpower']
p2._foo['clefable']['moves'] = ['moonblast', 'calmmind', 'softboiled', 'thunderwave']

# The battle_against method initiates a battle between two players.
# Here we are using asynchronous programming (await) to start the battle.
async def foo():
    await p1.battle_against(p2, n_battles = 1)

if(__name__ == "__main__"):
    import asyncio
    asyncio.run(foo())
