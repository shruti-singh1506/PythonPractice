import requests
import json

class PokemonNotFoundError(Exception):
    """Custom exception for handling when a user provided Pokemon input is not found"""
    def __init__(self, message="Couldn't catch em all!"):
        self.message = message
        super().__init__(self.message)

def get_pokemon_data(user_input):
    base_url = "https://pokeapi.co/api/v2/pokemon/"

    if user_input.isdigit():
        #User provided a number
        pokemon_url = f"{base_url}{user_input}/"
    else:
        #User provided a name - search if it exists
        all_pokemon_url = f"{base_url}?offset=0&limit=1302"
        response = requests.get(all_pokemon_url)
        if response.status_code !=200:
            raise PokemonNotFoundError("Failed to fetch Pokemon list.")
        
        all_pokemon_data = response.json()
        pokemon_entry = next((pokemon for pokemon in all_pokemon_data['results'] if pokemon['name'].lower() == user_input.lower()), None)

        if not pokemon_entry:
            raise PokemonNotFoundError()
        
        pokemon_url = pokemon_entry['url']

    #Fetch the data from the Pokemon's url
    response = requests.get(pokemon_url)
    if response.status_code != 200:
        raise PokemonNotFoundError()
    
    pokemon_data = response.json()

    #Save the data to a file
    with open("latest_query.json", "w") as file:
        json.dump(pokemon_data, file, indent=4)

    print(f"Data for {user_input} has been saved to latest_query.json")

if __name__ == "__main__":
    user_input = input("Enter the name or number of the Pokemon: ")
    try:
        get_pokemon_data(user_input)
    except PokemonNotFoundError as e:
        print(e.message)
    except Exception as e:
        print(f"An error has occured: {e}")

