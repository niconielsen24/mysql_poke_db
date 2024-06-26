import mysql.connector
from mysql.connector import Error
import pandas as pd

try:
    connection = mysql.connector.connect(
        user="root",
        password="nicanor24",
        host="localhost",
        database="pokemons"
    )
    print("Connection succesful")
except Error as err:
    print("Connection failed: ", err)
    exit(1)

cursor = connection.cursor()

tables = ["pokemon","abilities","types","moves","pokemon_abilities","pokemon_types","pokemon_moves"]

for table in tables:
    cursor.execute(f"DESCRIBE {table};")
    res = cursor.fetchall()
    df = pd.DataFrame(res,columns=["Field", "Type", "Null", "Key", "Default", "Extra"])
    print(f"Structure of table '{table}':\n{df}\n")

cursor.close()
connection.close()