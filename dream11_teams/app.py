from flask import Flask, render_template, request, redirect, session, jsonify
import random
import smtplib
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(10)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tharun@159",
  database="data",
)
mycursor=mydb.cursor()

@app.route("/")
def fun():
  return render_template('details.html')

@app.route("/home",methods=['POST'])
def hello_world():
        mycursor.execute('SELECT count(*) FROM players')
        count=mycursor.fetchall()
        print(count[0][0])
        my_teams=[]
        list = []
        names=[]
        if count[0][0]==0:
         for i in range(22):
           name=request.form.get(str(i+1))
           mycursor.execute("""INSERT INTO players (Name) VALUES ('{}')""".format(name))
           mydb.commit()
           names.append(name)
        else:
          for i in range(22):
             name = request.form.get(str(i+1))
             mycursor.execute("""UPDATE players SET Name='{}' WHERE Id={}""".format(name, i+1))
             mydb.commit()
             names.append(name)
        mycursor.execute('SELECT Name FROM players')
        names_list=mycursor.fetchall()
        
        my_teams_selected=[]
        identifier=[]
        for i in range(1, 23):
            list.append(i)
        while len(my_teams) <20:
         selected_list=[]
         while len(selected_list)<11:
            num = random.choice(list)
            if num not in selected_list:
             selected_list.append(num)

         selected_list.sort()
         sum=0
         mul=1
         for num in selected_list:
           sum+=num
           mul*=num
         if [sum,mul] not in identifier:
           my_teams.append(selected_list) 
           identifier.append([sum,mul])
          
        my_team_players=[]
        for teams in my_teams:
          temp=[]
          for id in teams:
           temp.append(names_list[id-1][0])
          my_team_players.append(temp)
        
           
        return render_template('home.html', players=my_team_players)


