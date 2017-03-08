from flask import Flask, render_template, url_for, request, redirect

import mysql.connector


app = Flask(__name__)

def db():
    con = mysql.connector.connect(user='alsoa', password='blomman123', host='192.168.48.244', database='watchedmovies')
    return con

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_movie")
def add_movie():
    return render_template("add_movie.html")

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

    return render_template("movie_library.html", movies=movies, time=movie_time)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/insert_movies', methods=['POST'])
def insert_movies():
    con = db()
    cursor = con.cursor()

    cursor.execute("""INSERT INTO movielist (name, genre, runtime, releasedate, rating) VALUES (%s, %s, %s, %s, %s)""",
                   (request.form['i_name'], request.form['i_genre'], request.form['i_runtime'], request.form['i_release_date'], request.form['i_rating']))
    cursor.close()
    con.commit()
    con.close()
    return redirect(url_for("movies"))

@app.route('/delete_movies', methods=['POST'])
def delete_movies():
    con = db()
    cursor = con.cursor()

    cursor.execute("""DELETE FROM movielist WHERE ID=%s""",
                   (request.form['movieid']))
    cursor.close()
    con.commit()
    con.close()
    return redirect(url_for("movies"))


if __name__ == "__main__":
    app.run()