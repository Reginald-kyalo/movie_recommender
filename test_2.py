from models import storage

movies = storage.all('MovieContentBased')
print([movie.title for movie in movies])