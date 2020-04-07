from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=False)
    release_year = db.Column(db.Integer, unique=False)
    rating = db.Column(db.String(8), unique=False)
    genre = db.Column(db.String(16), unique=False)
    starring = db.Column(db.String(32))

    def __init__(self, title, release_year, rating, genre, starring):
        self.title = title
        self.release_year = release_year
        self.rating = rating
        self.genre = genre
        self.starring = starring

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("title", "release_year", "rating", "genre", "starring")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# Endpoint to add new movie information
@app.route('/shareMovie', methods=['POST'])
def add_movie():
    title = request.json['title']
    release_year = request.json['release_year']
    rating = request.json['rating']
    genre = request.json['genre']
    starring = request.json['starring']

    new_movie = Movie(title, release_year, rating, genre, starring)

    db.session.add(new_movie)
    db.session.commit()

    movie = Movie.query.get(new_movie.id)

    return movie_schema.jsonify(guide)

# Endpoint to query all movies
@app.route('/viewMovies', methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()
    result = guides_schema.dump(all_movies)
    
    return jsonify(result)

# Endpoint to query a single movie
@app.route('/viewMovie', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    return movie_schema.jsonify(movie)

# Endpoint for 'putting' a movie
@app.route('/movie/<id>', methods=['PUT'])
def movie_update():
    movie = Movie.query.get(id)

    title = request.json['title']
    release_year = request.json['release_year']
    rating = request.json['rating']
    genre = request.json['genre']
    starring = request.json['starring']

    movie.title = title
    movie.release_year = release_year
    movie.rating = rating
    movie.genre = genre
    movie.starring = starring

    db.session.commit()
    return movie_schema.jsonify(movie)

@app.route('/movie/<id>', methods=['DELETE'])
def delete_movie():
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return movie_schema.jsonfiy(guide)

if __name__ == "__main__":
    app.run(debug=True)
