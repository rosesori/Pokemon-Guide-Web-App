import requests

# # generate all pokemon
listPokemon = []
response = requests.get("https://pokeapi.co/api/v2/pokedex/2/")
pokemonNames = response.json()
for pokemon in pokemonNames["pokemon_entries"]:
  listPokemon.append(pokemon["pokemon_species"]["name"])

# # collect and store routes by game
red_pokemon_routes = []
blue_pokemon_routes = []
for pokemon in listPokemon:
  red_routes = []
  blue_routes = []
  response = requests.get("https://pokeapi.co/api/v2/pokemon/%s/encounters" %pokemon)
  data = response.json()
  for i in data:
    # i["version_details"] returns a list of all versions
    for version in i["version_details"]:
      if (version["version"]["name"] == "red"):
        red_routes.append(i["location_area"]["name"])
      elif (version["version"]["name"] == "blue"):
        blue_routes.append(i["location_area"]["name"])
  red_pokemon_routes.append(red_routes)
  blue_pokemon_routes.append(blue_routes)

# # basic testing of routes
# # make sure the pokedex id of the pokemon is -1 because list is 0 index and pokemon id is 1 index
# for routes in red_pokemon_routes[16-1]: 
#   print(routes)

# # collect sprites and type information of the pokemon
sprite_urls = []
poke_types = []
for pokemon in listPokemon:
  pokeDatas = requests.get("https://pokeapi.co/api/v2/pokemon/%s/" %pokemon)
  pokeData = pokeDatas.json()
  sprite_urls.append(pokeData["sprites"]["front_default"])
  list_types = []
  for type_index in pokeData["types"]:
    list_types.append(type_index["type"]["name"])
  poke_types.append(list_types)

# # basic testing of sprite
# print("Sprite List Size:", len(sprite_urls))
# print("Pidgey URL:", sprite_urls[15])

# # basic testing of types
# print("Types Size:", len(poke_types))
# print(poke_types[15])

# pull all possible moves a pokemon can know that are machine learnable
learnable_moves_by_pokemon = []
all_unique_learnable_moves = set() # set
for pokemon in listPokemon:
  move_set = []
  pokeDatas = requests.get("https://pokeapi.co/api/v2/pokemon/%s/" %pokemon)
  move_list = pokeDatas.json()
  for move in move_list["moves"]:
    for version in move["version_group_details"]:
      if (version["move_learn_method"]["name"] == "machine") and (version["version_group"]["name"] == "red-blue"):
        # then add it to the list
        move_set.append(move["move"]["name"])
        all_unique_learnable_moves.add(move["move"]["name"])
  learnable_moves_by_pokemon.append(move_set)

# testing moves
# print(len(learnable_moves_by_pokemon))
# print(learnable_moves_by_pokemon[:10])

# count = 1
# for listMoves in learnable_moves_by_pokemon:
#   if not listMoves:
#     print(count, "-", listPokemon[count])
#   count += 1

# # pull HM/TM Information
moveInfoList = []
for move in all_unique_learnable_moves:
  move_to_tm = []
  move_to_tm.append(move)
  pokeDatas = requests.get("https://pokeapi.co/api/v2/move/%s/" %move)
  response = pokeDatas.json()
  for item in response["machines"]:
    if (item["version_group"]["name"] == "red-blue"):
      # get url from machine
      data = requests.get(item["machine"]["url"])
      tmInfo = data.json()
      move_to_tm.append(tmInfo["item"]["name"])
  moveInfoList.append(move_to_tm)

# Data Organization for batch insert
# POKEMON -> pokeID, pokemonName[listPokemon], red[routes], blue[routes], [poke_types], [learnableMoves], [sprite_urls]
database_formatted_list = []
if ((len(listPokemon) == 151) and (len(red_pokemon_routes) == 151) and (len(blue_pokemon_routes) == 151) and (len(poke_types) == 151) and (len(sprite_urls) == 151) and (len(learnable_moves_by_pokemon) == 151)):
  print("clean")
  for i in range(151):
    # ID, Name, rRoutes, bRoutes, types, mlMoves, sprite
    row = []
    row.append(i+1)
    row.append(listPokemon[i])
    row.append(red_pokemon_routes[i])
    row.append(blue_pokemon_routes[i])
    row.append(poke_types[i])
    row.append(learnable_moves_by_pokemon[i])
    row.append(sprite_urls[i])
    database_formatted_list.append(row)

# testing -> paste into notepad to see whole rows
print(database_formatted_list[0])
print(database_formatted_list[1])
print(database_formatted_list[15])

# MACHINE -> moveInfoList is perfect

# insert into database
print("Attempting Database Connection")
try:
    print("insert_query formatting begin...")
    connection = psycopg2.connect(user="postgres",
                                  password="pokemonyayy",
                                  host="database-1.c5fdsrfeeovx.us-east-2.rds.amazonaws.com",
                                  port="5432",
                                  database="myDatabase")
    cursor = connection.cursor()

    # create table if it doesn't exist
    cursor.execute("""CREATE TABLE pokemon(
    pokeid integer PRIMARY KEY,
    pokename text,
    redroutes text[],
    blueroutes text[],
    poketypes text[],
    mlmoves text[],
    sprite text
    );""")

    # insert pokemon info in pokemon database
    for row in database_formatted_list:
        insert_query = "insert into public.pokemon (pokeid, pokename, redroutes, blueroutes, poketypes, mlmoves, sprite)\nvalues ("
        id = "%i" %row[0]
        insert_query += id + "," # pokeid
        insert_query += "\'" + row[1] + "\'," # pokename
        insert_query += "\'{"
        entered = False
        for rRoute in row[2]: # redroutes
            entered = True
            insert_query += "\"" + rRoute + "\","
        if entered: # delete last comma
            insert_query = insert_query[:-1]
        entered = False
        insert_query += "}\',\'{"
        for bRoute in row[3]: # blueroutes
            entered = True
            insert_query += "\"" + bRoute + "\","
        if entered: # delete last comma
            insert_query = insert_query[:-1]
        entered = False
        insert_query += "}\',\'{"
        for type in row[4]: # poketypes
            entered = True
            insert_query += "\"" + type + "\","
        if entered: # delete last comma
            insert_query = insert_query[:-1]
        entered = False
        insert_query += "}\',\'{"
    
        for move in row[5]: # mlmoves
            entered = True
            insert_query += "\"" + move + "\","
        if entered: # delete last comma
            insert_query = insert_query[:-1]
        entered = False
        insert_query += "}\',\'" + row[6] + "\');"
        cursor.execute(insert_query)
        connection.commit()

    # insert machine moves
    for moveset in moveInfoList:
        cursor.execute("insert into public.machines (movename, machineid) values ('%s', '%s')"%(moveset[0], moveset[1]))
        connection.commit()

    print("Query ran successfully")
except (Exception, Error) as error:
    print("Query ran into an error:", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("Connection closed")
