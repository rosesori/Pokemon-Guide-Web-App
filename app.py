#from os import terminal_size
from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
import type
from type import *
from team import *

app = Flask(__name__)

def convert1D(array2D):
    array1D = []
    for i in array2D:
        for j in i:
            array1D.append(j)
    return array1D

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')

@app.route('/typeTutor', methods=["POST", "GET"])
def typeTutor():
    weakness = ""
    typestr = ""
    spriteUrl = ""
    if request.method == 'POST':
        pokemonName = (request.form['content']).lower()
        try:
            print("Insert_query formatting begin...")
            connection = psycopg2.connect(user="postgres",
                                        password="pokemonyayy",
                                        host="database-1.c5fdsrfeeovx.us-east-2.rds.amazonaws.com",
                                        port="5432",
                                        database="myDatabase")
            cursor = connection.cursor()

            insert_query = "SELECT type , sprite from pokemon where name = '%s';"%pokemonName
            cursor.execute(insert_query)
            info = cursor.fetchall()
            types = info[0][0]
            spriteUrl = info[0][1]
            moreThanOne = False
    
            for type in types:
                typestr += type + ", "
                moreThanOne = True
            if moreThanOne: 
                typestr = typestr[:-2]
                typestr = typestr.replace(",", "")
            weakness = getWeakness(typestr.split(" "))
         
        except (Exception) as error:
            print("Query ran into an error:", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("Connection closed")
        
    return render_template('typeTutor.html', types = weakness, sprite =  spriteUrl )

@app.route('/team', methods=["POST", "GET"])
def team():
    haveSubmitted = False
    hasWater = False
    hasFlying = False
    types = []
    pokemonList = []
    mic = False
    pokemonListMic = []
    p1 = ''
    p2 = ''
    p3 = ''
    p4 = ''
    p5 = ''
    p6 = ''
    print("Insert_query formatting begin...")
    connection = psycopg2.connect(user="postgres",
                                    password="pokemonyayy",
                                    host="database-1.c5fdsrfeeovx.us-east-2.rds.amazonaws.com",
                                    port="5432",
                                    database="myDatabase")
    cursor = connection.cursor()
    if request.method == 'POST':
        p1 = (request.form['poke1']).lower()
        p2 = (request.form['poke2']).lower()
        p3 = (request.form['poke3']).lower()
        p4 = (request.form['poke4']).lower()
        p5 = (request.form['poke5']).lower()
        p6 = (request.form['poke6']).lower()

    if p1=="" and p2=="" and p3=="" and p4=="" and p5=="" and p6=="":
        haveSubmitted = False
    else:
        haveSubmitted = True

    # make into list
    if p1 != "":
        pokemonList.append(p1)
    if p2 != "":
        pokemonList.append(p2)
    if p3 != "":
        pokemonList.append(p3)
    if p4 != "":
        pokemonList.append(p4)
    if p5 != "":
        pokemonList.append(p5)
    if p6 != "":
        pokemonList.append(p6)
    

    for pokemon in pokemonList:
        insert_query = "SELECT type from pokemon where name = '%s';"%pokemon 
        cursor.execute(insert_query)
        type = cursor.fetchall()
        type = type[0][0]
        types.append(type)
    
    types = convert1D(types)
    
    for type in types:
        if type == "water":
            hasWater = True
        if type == "flying":
            hasFlying = True
    
    return render_template('team.html', hasFlying = hasFlying, hasWater = hasWater, pokemonList = pokemonList, haveSubmitted=haveSubmitted)

@app.route('/HM&TM', methods=["POST", "GET"])
def item():
    correct = True
    userInput = ""
    item = ""

    if request.method == 'POST':
        userInput = (request.form['content']).lower()
        try:
            print("Insert_query formatting begin...")
            connection = psycopg2.connect(user="postgres",
                                        password="pokemonyayy",
                                        host="database-1.c5fdsrfeeovx.us-east-2.rds.amazonaws.com",
                                        port="5432",
                                        database="myDatabase")
            cursor = connection.cursor()

            insert_query = "SELECT moveid,type, name, machine from moves where type = '%s';"%userInput 
            cursor.execute(insert_query)
            item = cursor.fetchall()
            if len(item) == 0:
                correct = False
            else:
                correct = True
            # print(len())
        except (Exception) as error:
            print("Query ran into an error:", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("Connection closed")

    return render_template('item.html', items = item, correct = correct)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
