# This script is used to connect to PokeAPI so that we can gather and store all the moves in the Pokemon (Red/Blue) games.
# We need the moves so that we can also get their type info, which will be used on the HM/TM page.

import requests
import psycopg2

print("Starting script...")

# 1. Get all moves data from API-----------------------------------------------------------------------------------------------------------
response = requests.get("https://pokeapi.co/api/v2/move/?limit=844")
allMoves = response.json()

# 2. Get database columns using retrieved moves--------------------------------------------------------------------------------------------
print("Getting move names...")
moveNames = []
for move in allMoves["results"]:
    moveNames.append(move["name"])

print("Getting move types, move IDs, and corresponding machines...")
types = []
moveids = []
machines = []
for move in moveNames:
    moveMachine = ""
    response = requests.get("https://pokeapi.co/api/v2/move/%s" %move)
    moveData = response.json()
    types.append(moveData["type"]["name"])                          # Type
    moveids.append(moveData["id"])                                  # ID
    for machineVer in moveData["machines"]:
        if (machineVer["version_group"]["name"] == "red-blue"):
            machineURL = machineVer["machine"]["url"]
            machineResponse = requests.get(machineURL)
            machineData = machineResponse.json()
            moveMachine = machineData["item"]["name"]
    machines.append(moveMachine)                                    # Machine

# 3. Compile lists into one----------------------------------------------------------------------------------------------------------------
print("Compiling lists into one...")
database_formatted_list = []
if (len(moveNames)==844) and (len(types)==844) and (len(moveids)==844) and (len(machines)==844):
    print("Data lists were retrieved clean. All are same size.")
    for i in range(844):
        row = []
        row.append(moveids[i])
        row.append(moveNames[i])
        row.append(types[i])
        row.append(machines[i])
        database_formatted_list.append(row)

# 4. Insert into database-----------------------------------------------------------------------------------------------------------------
print("Attempting Database Connection...")
try:
    print("Insert_query formatting begin...")
    connection = psycopg2.connect(user="postgres",
                                  password="pokemonyayy",
                                  host="database-1.c5fdsrfeeovx.us-east-2.rds.amazonaws.com",
                                  port="5432",
                                  database="myDatabase")
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute("""CREATE TABLE moves(
    moveid integer PRIMARY KEY,
    name text,
    type text,
    machine text
    );""")

    # Insert move into moves table
    for row in database_formatted_list:
        insert_query = "insert into public.moves (moveid, name, type, machine)\nvalues ("

        # moveid
        id = "%i" %row[0]
        insert_query += id + ","

        # name
        insert_query += "\'" + row[1] + "\'," 
        
        # type
        insert_query += "\'" + row[2] + "\'," 

        # machine
        insert_query += "\'" + row[3] + "\');"

        cursor.execute(insert_query)
        connection.commit()

    print("Query ran successfully")
except (Exception) as error:
    print("Query ran into an error:", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("Connection closed")

