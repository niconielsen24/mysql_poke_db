import mysql.connector
from mysql.connector import Error
import pandas as pd

try:
    connection = mysql.connector.connect(
        user="root", 
        password="nicanor24", 
        host="localhost",
        )
    print("Connection succesful")
except Error as err: 
    print("Failed connection", err)
    exit(1)

cursor = connection.cursor()

create_db = "CREATE DATABASE pokemons;"

cursor.execute(create_db)

use_db = "USE pokemons;"

cursor.execute(use_db)

create_pokemons_table = """                        
CREATE TABLE IF NOT EXISTS pokemon(
    poke_id INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    base_xd INT DEFAULT 48,
    base_hp INT DEFAULT 48,
    base_attack INT DEFAULT 48,
    base_defense INT DEFAULT 48,
    base_sp_attack INT DEFAULT 48,
    base_sp_defense INT DEFAULT 48,
    speed INT DEFAULT 48,
    height INT,
    weight INT 
);
"""

create_abilities_table =  """
CREATE TABLE IF NOT EXISTS abilities(
    ability_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30)
);
"""

create_types_table = """
CREATE TABLE IF NOT EXISTS types(
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(15)
);
"""

create_moves_table = """
CREATE TABLE IF NOT EXISTS moves(
    move_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(15)
);
"""

create_pokemon_types =  """
CREATE TABLE IF NOT EXISTS pokemon_types(
    poke_id INT,
    type_id INT,
    PRIMARY KEY (poke_id, type_id),
    FOREIGN KEY (poke_id) REFERENCES pokemon(poke_id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES types(type_id) ON DELETE CASCADE
);
"""

create_pokemon_abilities = """
CREATE TABLE IF NOT EXISTS pokemon_abilities(
    poke_id INT,
    ability_id INT,
    PRIMARY KEY (poke_id, ability_id),
    FOREIGN KEY (poke_id) REFERENCES pokemon(poke_id) ON DELETE CASCADE,
    FOREIGN KEY (ability_id) REFERENCES abilities(ability_id) ON DELETE CASCADE
);
"""

create_pokemon_moves =  """
CREATE TABLE IF NOT EXISTS pokemon_moves(
    poke_id INT,
    move_id INT,
    PRIMARY KEY (poke_id, move_id),
    FOREIGN KEY (poke_id) REFERENCES pokemon(poke_id) ON DELETE CASCADE,
    FOREIGN KEY (move_id) REFERENCES moves(move_id) ON DELETE CASCADE
);
"""

cursor.execute(create_pokemons_table)
cursor.execute(create_abilities_table)
cursor.execute(create_types_table)
cursor.execute(create_moves_table)
cursor.execute(create_pokemon_types)
cursor.execute(create_pokemon_abilities)
cursor.execute(create_pokemon_moves)

cursor.execute("SHOW TABLES")

res = cursor.fetchall()
df = pd.DataFrame(res)
print(df)

cursor.close()
connection.close()