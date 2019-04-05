from flask import Flask, redirect, url_for, request, render_template
import sqlite3 as sql
import sqlite3

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
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        cur.execute("SELECT DISTINCT * from players WHERE (name, team) = (?,?)",[pname, tname])
        
        # cur.execute("SELECT * from players")
        print ("Table select successfully")
        rows = cur.fetchall()
    return render_template("listplayer.html",rows = rows)


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
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from players")
    print ("Table select successfully")

    rows = cur.fetchall()
    return render_template("listplayer.html",rows = rows)


@app.route('/init')
def init():
    conn = sqlite3.connect('database.db')
    print ("Opened database successfully")

    conn.execute('CREATE TABLE players (name TEXT, team TEXT, ssn TEXT)')
    print ("Table created successfully")
    conn.close()
    return 'OK'


if __name__ == '__main__':
    app.run(debug = True)









