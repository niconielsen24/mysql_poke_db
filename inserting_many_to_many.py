import mysql.connector
from mysql.connector import Error
import requests

def instert_many_to_many(connection,name,poke_id,types,abilities,moves):
    if connection.is_connected():
        cursor = connection.cursor()

        try:
            for poke_type in types:
                    insert_pokemon_type_query = """
                    INSERT IGNORE INTO pokemon_types(poke_id, type_id)
                    VALUES(%s,(
                        SELECT type_id FROM types WHERE name = %s LIMIT 1
                    ));
                    """
                    query_data = (poke_id,poke_type)
                    cursor.execute(insert_pokemon_type_query,query_data)

            for poke_ability in abilities:
                    insert_pokemon_ability_query = """
                    INSERT IGNORE INTO pokemon_abilities(poke_id, ability_id)
                    VALUES(%s,(
                        SELECT ability_id FROM abilities WHERE name = %s LIMIT 1
                    ));
                    """
                    query_data = (poke_id,poke_ability)
                    cursor.execute(insert_pokemon_ability_query,query_data)

            for poke_move in moves:
                    insert_pokemon_move_query = """
                    INSERT IGNORE INTO pokemon_moves(poke_id, move_id)
                    VALUES(%s,(
                        SELECT move_id FROM moves WHERE name = %s LIMIT 1
                    ));
                    """
                    query_data = (poke_id,poke_move)
                    cursor.execute(insert_pokemon_move_query,query_data)

            connection.commit()
            print(f"Relations for '{name}' inserted successfully.")
        except Error as err:
            print(f"Error inserting data: {err}")
            connection.rollback()
        finally:
             cursor.close()
    else:
        print("No connection to database available.")

try:
    connection = mysql.connector.connect(
        user="root",
        password="nicanor24",
        database="pokemons",
        host="localhost"
    )
    print("Connection successful")
except Error as err:
    print("Failed connection: ",err)
    exit(1)

response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')

if response.status_code == 200:
    data = response.json()

    names = [pokemon['name'] for pokemon in data['results']]
    filtered_names = [name for name in names if '-' not in name]

    for name in filtered_names:
        poke = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        if poke.status_code == 200:
            poke_data = poke.json()
            include_fields = ["id","name","types","abilities","moves"]
            filtered_poke = {key: poke_data[key] for key in poke_data.keys() if key in include_fields}

            poke_id = filtered_poke.get("id")
            name = filtered_poke.get("name")
            types = [type['type']['name'] for type in filtered_poke.get("types", [])]
            abilities = [ability['ability']['name'] for ability in filtered_poke.get("abilities", [])]
            moves = [move['move']['name'] for move in filtered_poke.get("moves", [])]

            instert_many_to_many(connection,name,poke_id,types,abilities,moves)

        else:
            print(f"Failed to retrieve {name} data, status code : ", poke.status_code)

else:
    print("Failed to get PokeAPI data, status code : ", response.status_code)