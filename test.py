import mysql.connector 
from mysql.connector import Error
import pandas as pd

connection = mysql.connector.connect(
        user="root",
        password="nicanor24",
        database="pokemons",
        host="localhost"
    )

cursor = connection.cursor()

cursor.execute("SELECT COUNT(poke_id) FROM pokemon;")
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["Number of P"])
print(df)

cursor.execute("SELECT COUNT(move_id) FROM moves;")
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["Number of M"])
print(df)

cursor.execute("SELECT COUNT(type_id) FROM types;")
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["Number of T"])
print(df)

cursor.execute("SELECT COUNT(ability_id) FROM abilities;")
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["Number of A"])
print(df)

cursor.execute("SELECT COUNT(move_id) FROM pokemon_moves;")
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["Number of p_M"])
print(df)

cursor.execute("SELECT COUNT(type_id) FROM pokemon_types;")
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["Number of p_T"])
print(df)

cursor.execute("SELECT COUNT(ability_id) FROM pokemon_abilities;")
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["Number of p_A"])
print(df)

query = """
        SELECT * FROM abilities
        WHERE ability_id IN (
            SELECT ability_id FROM pokemon_abilities
            WHERE poke_id = 6
            );
        """

cursor.execute(query)
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["ability_id","Name"])
print(df)

query = """
        SELECT * FROM moves
        WHERE move_id IN (
            SELECT move_id FROM pokemon_moves
            WHERE poke_id = 6
            );
        """

cursor.execute(query)
res = cursor.fetchall()
df = pd.DataFrame(res,columns=["move_id","Name"])
print(df)

cursor.close()
connection.close()