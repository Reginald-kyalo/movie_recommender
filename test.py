from models import storage
from preprocessing import load_csv

#load_csv("/home/reginald/reg_codes/webstack_portfolio_project/movie_recommender/tmdb_5000_movies.csv")
load_csv("/home/reginald/reg_codes/webstack_portfolio_project/movie_recommender/tmdb_5000_credits.csv")
##cls = 'Movie'
##movie = storage.get_item_by_id(cls, 102651)
##if movie:
##    print(movie.to_dict())
##else:
##    print("not found")