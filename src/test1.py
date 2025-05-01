from poke_env.player.random_player import RandomPlayer
from poke_env.player.max_damage_player import MaxDamagePlayer
from poke_env.ps_client import ShowdownServerConfiguration, AccountConfiguration
from poke_env.data import GenData

snorlax = """
Snorlax @ Expert Belt
Ability: Thick Fat
Tera Type: Normal
EVs: 252 HP / 252 Atk / 4 Def
Adamant Nature
- Fire Punch
- Ice Punch
- Heavy Slam
- Body Slam
"""

scizor = """
Scizor @ Iron Plate
Ability: Technician
Tera Type: Bug
EVs: 252 Atk / 4 SpD / 252 Spe
Adamant Nature
- Bullet Punch
- Close Combat
- Counter
- Agility
"""

mence = """
Salamence @ Sky Plate
Ability: Moxie
Tera Type: Dragon
EVs: 252 Atk / 164 Def / 4 SpD / 88 Spe
Adamant Nature
- Temper Flare
- Outrage
- Dual Wingbeat
- Iron Head
"""

gard = """
Gardevoir @ Choice Specs
Ability: Trace
Tera Type: Psychic
EVs: 4 Def / 252 SpA / 252 Spe
Modest Nature
IVs: 0 Atk
- Moonblast
- Mystical Fire
- Aura Sphere
- Psyshock
"""

# The RandomPlayer is a basic agent that makes decisions randomly,
# serving as a starting point for more complex agent development.
first_player = MaxDamagePlayer(
    ##server_configuration = ShowdownServerConfiguration,
    account_configuration = AccountConfiguration("Lechode", "TY5WMfgR9DMX3Dr"),
    save_replays = "C:\\Users\\KYRIAKOS\\Music\\poke-env\\replays",
    battle_format="gen9nationaldex",
    team = scizor,
    opp_team = gard
)
second_player = MaxDamagePlayer(
    ##server_configuration = ShowdownServerConfiguration,
    account_configuration = AccountConfiguration("nacrotic", "TY5WMfgR9DMX3Dr"),
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
