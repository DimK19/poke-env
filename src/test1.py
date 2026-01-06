from poke_env.player.random_player import RandomPlayer
from poke_env.player.max_damage_player import MaxDamagePlayer
from poke_env.ps_client import ShowdownServerConfiguration, AccountConfiguration
from poke_env.data import GenData
from poke_env.data.teams import gard, scizor

from configparser import ConfigParser

config = ConfigParser()
config.read('C:\\Users\\KYRIAKOS\\Documents\\poke-env\\config.ini', encoding = 'utf-8')

# The RandomPlayer is a basic agent that makes decisions randomly,
# serving as a starting point for more complex agent development.
first_player = MaxDamagePlayer(
    ##server_configuration = ShowdownServerConfiguration,
    account_configuration = AccountConfiguration(config['PLAYER 1']['USERNAME'],
                                                 config['PLAYER 1']['PASSWORD']),
    save_replays = "C:\\Users\\KYRIAKOS\\Music\\poke-env\\replays",
    battle_format="gen9nationaldex",
    team = scizor,
    opp_team = gard
)
second_player = MaxDamagePlayer(
    ##server_configuration = ShowdownServerConfiguration,
    account_configuration = AccountConfiguration(config['PLAYER 2']['USERNAME'],
                                                 config['PLAYER 2']['PASSWORD']),
    battle_format="gen9nationaldex",
    team = gard,
    opp_team = scizor
)

# The battle_against method initiates a battle between two players.
# Here we are using asynchronous programming (await) to start the battle.
async def foo():
    await first_player.battle_against(second_player, n_battles = 1)

if(__name__ == "__main__"):
    import asyncio
    asyncio.run(foo())
