#!/usr/bin/python3
from recommender import recommend
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/movielike', methods=['GET'])
def recommendation():
    """
    Endpoint to provide movie recommendations based on a given title.

    This endpoint accepts a GET request with a 'title' query parameter, which is used
    to retrieve a list of recommended movies from the `recommend` function. The recommendations
    are returned in JSON format. If an error occurs (such as a missing title or no recommendations
    available), the response includes an error message and an appropriate status code.

    Query Parameters:
        title (str): The movie title to base recommendations on.

    Returns:
        JSON response with one of the following:
        - A list of recommended movies (if recommendations are found), in JSON format.
        - An error message with a 400 status code if no recommendations are found.
        - An error message with a 500 status code if an unexpected error occurs.

    Example Usage:
        GET /recommend?title=inception
    """
    title = request.args.get('title')

    if not title:
        return jsonify({"error": "Movie Title is required."}), 400

    title = title.lower()

    recommendations = recommend(title)
    
    if not recommendations:
        return jsonify({"error": "No recommendations found for the provided title."}), 400

    if not isinstance(recommendations, (dict, list)):
        return jsonify({"error": "An unexpected error occurred"}), 500

    if isinstance(recommendations, list) and isinstance(recommendations[0], str):
        return jsonify({"error": recommendations[0]}), 400

    return jsonify(recommendations)
if __name__ == '__main__':
    app.run(debug=True)
