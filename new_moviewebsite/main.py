from flask import Flask, render_template, url_for, request, redirect, session, flash, wrappers


import mysql.connector

app = Flask(__name__)


def db():
    con = mysql.connector.connect(user='alsoa', password='blomman123', host='192.168.48.244', database='watchedmovies')
    return con


@app.route("/")
def home():
    session
    return render_template("index.html")

@app.route("/add_movie")
def add_movie():
    if 'username' in session:
        return render_template("add_movie.html")
    else:
        return render_template("login.html")

@app.route("/movies")
def movies():
    # Establish communication with db
    con = db()
    cursor = con.cursor()

    # Om seeeion är skapad och innehåller userid
    # ställ DB-fråga med userid
    # annars skicka till login

    # Execute and fetch data
    cursor.execute("SELECT id, name, genre, runtime, releasedate, rating, timeswatched FROM movielist WHERE userid = %s",
        [session['userid']])
    movies = cursor.fetchall()

    #Calculate time user have watched movies in hours
    movie_time = 0
    for i in movies:
        movie_time = (movie_time + i[3] * i[6])
    movie_time = (movie_time/60)


    cursor.close()
    con.close()

    if 'username' in session:
        return render_template("movie_library.html", movies=movies, time=movie_time)
    else:
        return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/editmovie", methods = ['POST'])
def editmovie():
    con = db()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM movielist WHERE id='"+request.form['i_edit']+"'")
    movie_details = cursor.fetchall()
    cursor.close()
    con.commit()
    con.close()

    if 'username' in session:
        return render_template("editmovie.html",movie_details=movie_details)
    else:
        return render_template("login.html")


@app.route('/insertmovie', methods=['POST'])
def insertmovie():
    con = db()
    cursor = con.cursor()

    cursor.execute("""INSERT INTO movielist (name, genre, runtime, releasedate, rating, timeswatched, userid) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                   (request.form['i_name'], request.form['i_genre'], request.form['i_runtime'], request.form['i_release_date'], request.form['i_rating'], request.form['i_timeswatched'], session['userid']))
    cursor.close()
    con.commit()
    con.close()
    return redirect(url_for("movies"))


@app.route('/removemovie', methods=['POST'])
def removemovie():
    con = db()
    cursor = con.cursor()

    cursor.execute("DELETE FROM movielist WHERE id='"+request.form['movieid']+"'")

    cursor.close()
    con.commit()
    con.close()
    return redirect(url_for("movies"))


@app.route('/updatemovie', methods=['POST'])
def updatemovie():
    con = db()
    cursor = con.cursor()

    cursor.execute("UPDATE movielist SET name='"+request.form['i_name']+"', genre='"+request.form['i_genre']+"', runtime='"+\
                    request.form['i_runtime']+"', releasedate='"+request.form['i_release_date']+"', rating='"+request.form['i_rating']+"', timeswatched='"+request.form['i_timeswatched']+"'\
                    WHERE id='"+request.form['movieid']+"'")

    cursor.close()
    con.commit()
    con.close()
    return redirect(url_for('movies'))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():

    return render_template("signup.html")


@app.route('/insertuser', methods=['POST'])
def insertuser():
    con = db()
    cursor = con.cursor()

    cursor.execute("INSERT INTO users (user_username, user_password) VALUES (%s, %s)",
                   (request.form['u_username'], request.form['u_password']))
    cursor.close()
    con.commit()
    con.close()
    return render_template('login.html')


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if 'username' in session:
        print("logged in")
        return redirect(url_for('home'))
    if request.method == 'POST':
        con = db()
        print("printa DA")
        cursor = con.cursor()
        username_form = request.form['u_username']
        password_form = request.form['u_password']
        cursor.execute("SELECT COUNT(1) FROM users WHERE user_username = %s;", [username_form])
        if cursor.fetchone()[0]:
            cursor.execute("SELECT user_password, user_id FROM users where user_username = %s", [username_form])
            for row in cursor.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['u_username']
                    session['userid'] = row[1]
                    return redirect(url_for('home'))

        cursor.close()
        con.commit()
        con.close()
    return redirect(url_for('login', error="wrong username or password"))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

app.secret_key = 'DAS/SECRET/KEY'

if __name__ == "__main__":
    app.run(debug=True, port=5002)