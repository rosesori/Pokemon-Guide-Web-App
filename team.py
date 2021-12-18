import psycopg2

# this file outputs team members given a pokemon
# type list is not necessary with current implementation
# type = ["normal", "fire", "water", "electric", "grass", "ice", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon"]

# var to check if there are any errors in query/input
error = False # passing this
noVal = True

# starting database connection to pull type info
def hasFlyingWater(userPokemon): # frontend user-input of pokemon
    if hasFlying(userPokemon) and hasWater(userPokemon):
        return True
    return False

def hasFlying(userPokemon):
    global noVal
    global error
    try:
        print("Insert_query formatting begin...")
        connection = psycopg2.connect(user="postgres",
                                    password="pokemonyayy",
                                    host="database-1.c5fdsrfeeovx.us-east-2.rds.amazonaws.com",
                                    port="5432",
                                    database="myDatabase")
        cursor = connection.cursor()
        print("Has flying: ", userPokemon)
        for pokemon in userPokemon:
            insert_query = "SELECT type from pokemon where name = '%s';"%pokemon 
            cursor.execute(insert_query)
            types = cursor.fetchall()
            for type in types:
                if type.lower() == "flying":
                    return True
        else:
            noVal = True
            return False
    except Exception as error:
        print("Query ran into an error:", error)
        error = True
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed")
    return False

def hasWater(userPokemon):
    global noVal
    global error
    try:
        print("Insert_query formatting begin...")
        connection = psycopg2.connect(user="postgres",
                                    password="pokemonyayy",
                                    host="database-1.c5fdsrfeeovx.us-east-2.rds.amazonaws.com",
                                    port="5432",
                                    database="myDatabase")
        cursor = connection.cursor()
        print("Has water: ", userPokemon)
        for pokemon in userPokemon:
            insert_query = "SELECT type from pokemon where name = '%s';"%pokemon 
            cursor.execute(insert_query)
            types = cursor.fetchall()
            for type in types:
                if type.lower() == "water":
                    return True
        else:
            noVal = True
            return False
    except Exception as error:
        print("Query ran into an error:", error)
        error = True
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed")
    return False

def hasError():
    return error

def hasNoVal():
    return noVal