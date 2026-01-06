import requests

URL_DAMAGE_CALC = "http://localhost:8060/calculate"

def _get_damage_calc(
    spec: str,
    item: str,
    nat: str,
    ab: str,
    evs: dict,
    boosts: dict,
    move: str,
    opp: str,
    opp_item: str,
    opp_nat: str,
    opp_ab: str,
    opp_evs: dict,
    opp_boosts: dict
):
    if(not boosts):
        boosts = {}
    if(not opp_boosts):
        opp_boosts = {}

    payload = {
        "attacker": {
            "species": spec,
            "item": item,
            "nature": nat,
            "ability": ab,
            "evs": evs,
            "boosts": boosts
        },
        "defender": {
            "species": opp,
            "item": opp_item,
            "nature": opp_nat,
            "ability": opp_ab,
            "evs": opp_evs,
            "boosts": opp_boosts
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

async def _get_max_damage_move(attacker, defender, moves):
    """
    Finds the move that deals the most damage among the list.
    """
    
    ## Send requests to damage calc middleware to get damage calculations for each move
    options = {}
    for m in moves:
        damage = _get_damage_calc(
            spec = attacker['species'],
            item = attacker['item'],
            nat = attacker['nature'],
            ab = attacker['ability'],
            evs = attacker['evs'],
            boosts = attacker['boosts'],
            move = m,
            opp = defender['species'],
            opp_item = defender['item'],
            opp_nat = defender['nature'],
            opp_ab = defender['ability'],
            opp_evs = defender['evs'],
            opp_boosts = defender['boosts']
        )

        options[m] = damage

        ## #print(f'My {m._id} does {damage}')
    ## Choose max damage
    best_move = max(moves, key = lambda m: options[m])

    return best_move, options[best_move]
