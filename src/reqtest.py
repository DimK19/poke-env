import requests

# URL of your server
url = 'http://localhost:8060/calculate'

# Data payload
payload = {
    "attacker": {
        "species": "Gengar",
        "item": "Choice Specs",
        "nature": "Timid",
        "evs": { "spa": 252 },
        "boosts": { "spa": 1 }
    },
    "defender": {
        "species": "Chansey",
        "item": "Eviolite",
        "nature": "Calm",
        "evs": { "hp": 252, "spd": 252 }
    },
    "move": {
        "name": "Focus Blast"
    }
}

# Send POST request
response = requests.post(url, json = payload)

# Print the server's response
print('Status Code:', response.status_code)
print('Response JSON:', response.json())
