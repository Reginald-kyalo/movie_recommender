# Movie Recommendation App

This app is designed to provide personalized movie recommendations based on user preferences and past viewing history. It utilizes data processing and machine learning techniques to analyze movies and suggest those that may align with the user's interests.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Data Preprocessing**: Prepares and cleans data to be used in the recommendation algorithm.
- **Movie Recommendations**: Provides suggestions based on user preferences and/or viewing history.
- **Database Management**: Manages movie and user data using SQLAlchemy and integrates foreign key relationships to ensure efficient data retrieval.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Reginald-kyalo/movie_recommender.git
   cd movie_recommender
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Setting DATABASE_URL for Database Access**
   ```bash
   export DATABASE_URL="postgresql://moviedb_owner:MQnG7pADat3y@ep-restless-mouse-a8zehkhu.eastus2.azure.neon.tech/moviedb?sslmode=require"
   ```

## Usage

1. **Run the main application**:
   ```bash
   flask run app
   curl -X GET "http://127.0.0.1:5000/movielike?title=<movie-title>" Movie title eg.. Inception
   ```

2. **Customization**: Modify configurations or settings in `app.py` to adjust recommendation criteria or url parameters.

## Project Structure

- **app.py**: Main entry point for the app, managing user interactions and recommendations.
- **preprocessing.py**: Contains functions for data cleaning and preprocessing.
- **recommender.py**: Core recommendation algorithm, responsible for generating movie suggestions.
- **movie.py**: Defines the database schema and interactions with SQLAlchemy.
- **credit.py**: Defines the database schema and interactions with SQLAlchemy.
- **movie_content_based.py**: Defines the database schema and interactions with SQLAlchemy.
- **db_storage.py**: Manages the database connection, session, and data manipulation for SQLAlchemy models.

## Dependencies

- Python 3.x
- SQLAlchemy
- Flask

- Additional dependencies specified in `requirements.txt`

## Contributing

Contributions are welcome! Please submit a pull request or raise issues for any bugs or new features.

## License

This project is licensed under the MIT License.

---