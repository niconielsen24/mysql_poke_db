import requests
import json
import mysql.connector
from mysql.connector import Error

def insert_pokemon(id, name, height, weight, base_xp, abilities, moves, types, stats, connection):
    if connection.is_connected():
        cursor = connection.cursor()
        try:
            insert_pokemon_query = """
            INSERT INTO pokemon (poke_id, name, base_xd, base_hp, base_attack,
                                  base_defense, base_sp_attack, base_sp_defense, speed, height, weight)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            poke_data = (id, name, base_xp, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], height, weight)
            cursor.execute(insert_pokemon_query, poke_data)

            # Insert abilities (if not exists)
            for ability in abilities:
                insert_ability_query = """
                INSERT IGNORE INTO abilities (name)
                VALUES (%s)
                """
                ab_data = (ability,)
                cursor.execute(insert_ability_query, ab_data)

            # Insert moves (if not exists)
            for move in moves:
                insert_move_query = """
                INSERT IGNORE INTO moves (name)
                VALUES (%s)
                """
                mv_data = (move,)
                cursor.execute(insert_move_query, mv_data)

            # Insert types (if not exists)
            for type in types:
                insert_type_query = """
                INSERT IGNORE INTO types (name)
                VALUES (%s)
                """
                tp_data = (type,)
                cursor.execute(insert_type_query, tp_data)

            connection.commit()
            print(f"Pokemon '{name}' inserted successfully.")

        except Error as err:
            print(f"Error inserting data: {err}")
            print(err._full_msg)
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
    print("Connection failed: ", err)
    exit(1)

try:
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')

    if response.status_code == 200:
        data = response.json()
        names = [pokemon['name'] for pokemon in data['results']]
        filtered_names = [name for name in names if '-' not in name]

        for name in filtered_names:
            poke_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
            poke_json = poke_response.json()
            include_fields = ["id", "name", "moves", "abilities", "weight", "height", "types", "stats", "base_experience"]
            filtered_poke = {key: poke_json[key] for key in poke_json.keys() if key in include_fields}

            id = filtered_poke.get("id")
            name = filtered_poke.get("name")
            weight = filtered_poke.get("weight", 0)
            height = filtered_poke.get("height", 0)
            base_experience = filtered_poke.get("base_experience", 0)

            abilities = [ability['ability']['name'] for ability in filtered_poke.get("abilities", [])]
            moves = [move['move']['name'] for move in filtered_poke.get("moves", [])]
            types = [type['type']['name'] for type in filtered_poke.get("types", [])]
            stats = [stat['base_stat'] for stat in filtered_poke.get("stats", [])]

            insert_pokemon(id, name, height, weight, base_experience, abilities, moves, types, stats, connection)

    else:
        print('Failed to retrieve Pokémon data from the PokeAPI')

except requests.exceptions.RequestException as e:
    print(f"Error with HTTP request: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
