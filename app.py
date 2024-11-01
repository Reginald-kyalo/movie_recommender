from flask import Flask, request, jsonify
from recommender import recommend
app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommendation():
    title = request.args.get('title').lower()
 
    recommendations = recommend(title)
    
    if isinstance(recommendations, list) and isinstance(recommendations[0], str):
        return jsonify({"error": recommendations[0]}), 400  # Handle error message

    return jsonify(recommendations)
if __name__ == '__main__':
    app.run(debug=True)
