#!/usr/bin/python3
"""Generate movie recommendations based on content based filtering
"""
from preprocessing import process_data
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ps = PorterStemmer()
def stem(text):
    """
    Apply stemming to each word in a given text string.

    This function takes a string, splits it into individual words, applies the Porter stemming algorithm to each word,
    and then joins the stemmed words back into a single string.

    Parameters:
        text (str): The input text to be stemmed.

    Returns:
        str: The stemmed version of the input text, with each word reduced to its root form.
    """
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def recommend(movie):
    """
    Generate movie recommendations based on similarity to a specified movie.

    This function processes a dataset of movies to generate a list of recommended movies similar to the specified
    title based on content-based filtering. The process includes data preprocessing, vectorization, and similarity
    calculation.

    Parameters:
        movie (str): The title of the movie for which recommendations are to be generated.

    Returns:
        list: A list of dictionaries containing recommended movies and their details.
              Each dictionary contains information about a recommended movie.
              If an error occurs (e.g., movie not found), a list with an error message is returned.

    Exceptions:
        If the movie title is not found in the database, it returns a list with the message ["Movie not found in the database."].
        If other errors occur during processing, it returns a list with the exception message.

    Example Response:
        [
            {
                "movie_id": 123,
                "title": "Interstellar",
                "genres": ["Sci-Fi", "Adventure"],
                "keywords": ["space", "time travel"],
                "cast": ["Matthew McConaughey", "Anne Hathaway"],
                "director": ["Christopher Nolan"],
                "overview": "A team of explorers travel through a wormhole in space..."
            },
            ...
        ]
    """
    try:
        movies = process_data(movie)
        original_movies = movies.copy()
    except Exception as e:
        return [e]

    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    for col in ['genres', 'keywords', 'cast', 'director']:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['director']
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

    new_df = movies[['movie_id', 'title', 'tags']].copy()

    new_df['tags'] = new_df['tags'].apply(stem)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()

    # print(cv.get_feature_names_out())

    similarity = cosine_similarity(vectors)

    try:
        movie_index = new_df[new_df['title'].str.lower() == movie.lower()].index[0]
    except IndexError:
        return ["Movie not found in the dataframe."]

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = [original_movies.iloc[i[0]] for i in movies_list]
    recommendations_list = [{k: v for k, v in rec.to_dict().items() if k != '__class__'} for rec in recommendations]
    return recommendations_list
