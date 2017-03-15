from flask import Flask, render_template, url_for, request, redirect, session, flash, wrappers


import mysql.connector

app = Flask(__name__)
app.secret_key = 'Apples'

def db():
    con = mysql.connector.connect(user='alsoa', password='blomman123', host='192.168.48.244', database='watchedmovies')
    return con


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_movie")
def add_movie():
    if session['logged_in'] == True:
        return render_template("add_movie.html")
    else:
        return render_template("login.html")

@app.route("/movies")
def movies():
    # Establish communication with db
    con = db()
    cursor = con.cursor()

    # Execute and fetch data
    cursor.execute("SELECT id, name, genre, runtime, releasedate, rating FROM movielist")
    movies = cursor.fetchall()

    #Calculate time user have watched movies in hours
    movie_time = 0
    for i in movies:
        movie_time = (movie_time + i[3])
    movie_time = round(movie_time/60)

    cursor.close()
    con.close()

    if session['logged_in'] == True:
        return render_template("movie_library.html", movies=movies, time=movie_time)
    else:
        return render_template("login.html")

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

    if session['logged_in'] == True:
        return render_template("editmovie.html",movie_details=movie_details)
    else:
        return render_template("login.html")


@app.route('/insertmovie', methods=['POST'])
def insertmovie():
    con = db()
    cursor = con.cursor()

    cursor.execute("""INSERT INTO movielist (name, genre, runtime, releasedate, rating) VALUES (%s, %s, %s, %s, %s)""",
                   (request.form['i_name'], request.form['i_genre'], request.form['i_runtime'], request.form['i_release_date'], request.form['i_rating']))
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
                    request.form['i_runtime']+"', releasedate='"+request.form['i_release_date']+"', rating='"+request.form['i_rating']+"'\
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


@app.route('/loginuser', methods=['POST'])
def loginuser():
    con = db()
    cursor = con.cursor()


    cursor.execute("SELECT * FROM users where user_username ='" + request.form['u_username'] + "' and user_password ='" + request.form['u_password'] + "'")
    data = cursor.fetchone()

    cursor.close()
    con.commit()
    con.close()

    if data is None:
        return "Username or password is wrong"
    else:
        session['logged_in'] = True
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(port=5001)