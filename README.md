# ReadNext

ReadNext is a sophisticated book recommendation system that leverages user ratings to suggest top-rated books and provide personalized recommendations.

## Features

- **Top Books Section:** Displays the top 50 books based on user ratings.
- **Search Functionality:** Allows users to search for books using partial or full titles.
- **Personalized Recommendations:** Offers book suggestions based on similarity scores derived from user ratings.
- **Fallback Recommendations:** Provides author and publisher recommendations if a queried book is not in the top-rated list.

## Related Projects

### Book Recommender System

The [Book Recommender System](https://github.com/thepritamshaw/ML/tree/master/Book_Recommender_System) project, part of my ML repository, is where the calculations and initial data processing for ReadNext's recommendation engine were performed. It includes detailed Jupyter Notebook files with analysis and the original datasets used for training.

## Data Sources

- The dataset is sourced from [Kaggle's Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset), which includes `users.csv`, `books.csv`, and `ratings.csv`.

## Implementation Details

- **Top Books Calculation:** Uses SQL-like commands in Python to determine the top 50 books.
- **Similarity Matrix:** A 706x810 matrix calculates similarity scores using cosine similarity in a user-book ratings matrix.
- **Fallback Logic:** Suggests books by the same author or publisher if the query does not match top-rated books.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/thepritamshaw/ReadNext.git
    cd ReadNext
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
