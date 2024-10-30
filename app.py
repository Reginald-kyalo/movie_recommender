from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title').lower()
    
    # Fetch movie_id for the requested title
    movie = session.query(Movie).filter(Movie.title.ilike(title)).first()
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    # Find the index of the requested movie in the loaded vectors
    movie_index = movie_ids.index(movie.movie_id)
    
    # Get similarity scores and sort them
    distances = similarity[movie_index]
    similar_movies = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    # Fetch movie titles for the recommendations
    recommendations = [
        session.query(Movie).get(movie_ids[i[0]]).title for i in similar_movies
    ]
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
