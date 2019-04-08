from flask import Flask, redirect, url_for, request, render_template
import sqlite3 as sql
import sqlite3

from sqlalchemy import *
DATABASEURI = "postgresql://yw3225:dbdb@34.73.21.127/proj1part2"

app = Flask(__name__)

# @app.route('/admin')
# def hello_admin():
#     return 'Hello Admin'

# @app.route('/searchplayer/<name>')
# def player_info(name):
#     return 'Hello %s as Player' % name


# @app.route('/hello/<name>')
# def show_player(name):
#     return render_template('hello.html', pname = name)



@app.route('/result',methods = ['POST', 'GET'])
def search_player():
    if request.method == 'POST':
        pname = request.form['pname']
        tname = request.form['tname']
        print(tname, pname)
        
        # con = sql.connect("database.db")
        # con.row_factory = sql.Row
        # cur = con.cursor()

        engine = create_engine(DATABASEURI, convert_unicode=True)
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        # conn.execute("CREATE VIEW viewplayer AS SELECT pid,players.team,players.ssn,birthday,height_in,weight_lb,position,salary2018_2019,pointspergame FROM players inner join employees on players.ssn = employees.ssn")
        # rows = cursor_player.fetchall()
        players = Table('viewplayer', metadata, autoload=True)
        rows_player = players.select(players.c.pid == pname).execute()

        # metadata = MetaData(bind=engine)
        # players = Table('players', metadata, autoload=True)
        # rows = players.select(players.c.pid == pname).execute()

        # cur.execute("SELECT * from players")
        print ("Table select successfully")
    return render_template("psqlsearch.html",rows_player = rows_player)


# @app.route('/result',methods = ['POST', 'GET'])
# def result():
#     if request.method == 'POST':
#         result = request.form
#         return render_template("search.html",result = result)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/enterplayer')
def new_player():
    return render_template('newplayer.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
       try:
          nm = request.form['addname']
          tm = request.form['addteam']
          pssn = request.form['addssn']

          with sql.connect("database.db") as con:
             cur = con.cursor()
             cur.execute("INSERT INTO players (name, team, ssn) VALUES (?,?,?)",(nm,tm,pssn) )

             con.commit()
             msg = "Record successfully added"
       except:
          con.rollback()
          msg = "error in insert operation"

       finally:
          return render_template("result.html",msg = msg)
          con.close()


@app.route('/listplayer')
def listplayer():
    # con = sql.connect("database.db")
    # con.row_factory = sql.Row
    # cur = con.cursor()
    # cur.execute("select * from players")
    # rows = cur.fetchall()

    engine = create_engine(DATABASEURI)
    conn = engine.connect()
    cursor_player = conn.execute("select * from players inner join employees on players.ssn = employees.ssn")
    rows_player = cursor_player.fetchall()
    return render_template("listplayer.html",rows = rows_player)

@app.route('/listteam')
def listteam():
    engine = create_engine(DATABASEURI)
    conn = engine.connect()
    cursor_team = conn.execute("select * from teams")
    rows_team = cursor_team.fetchall()
    return render_template("listteam.html",rows = rows_team)

@app.route('/listgame')
def listgame():
    engine = create_engine(DATABASEURI)
    conn = engine.connect()
    cursor_game = conn.execute("select * from games")
    rows_game = cursor_game.fetchall()
    return render_template("listgame.html",rows = rows_game)


@app.route('/init')
def init():
    conn = sqlite3.connect('database.db')
    print ("Opened database successfully")

    conn.execute('CREATE TABLE players (name TEXT, team TEXT, ssn TEXT)')
    print ("Table created successfully")
    conn.close()
    return 'OK'


@app.route('/initpsql')
def initpsql():
    engine = create_engine(DATABASEURI)
    conn = engine.connect()

    cursor_player = conn.execute("select * from players inner join employees on players.ssn = employees.ssn")
    rows_player = cursor_player.fetchall()

    cursor_coach = conn.execute("select * from coaches inner join employees on coaches.ssn = employees.ssn")
    rows_coach = cursor_coach.fetchall()

    cursor_manager = conn.execute("select * from managers inner join employees on managers.ssn = employees.ssn")
    rows_manager = cursor_manager.fetchall()

    cursor_team = conn.execute("select * from teams")
    rows_team = cursor_team.fetchall()

    cursor_boss = conn.execute("select * from boss")
    rows_boss = cursor_boss.fetchall()

    cursor_game = conn.execute("select * from games")
    rows_game = cursor_game.fetchall()

    return render_template("list.html", 
      rows_player=rows_player, 
      rows_coach=rows_coach,
      rows_manager=rows_manager,
      rows_team=rows_team,
      rows_boss=rows_boss,
      rows_game=rows_game)


if __name__ == '__main__':
    app.run(debug = True)









