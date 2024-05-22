from django.shortcuts import render
import pandas as pd
import json, difflib

# Create your views here.
def index(request):
	csv_file_path = 'data/popular_books.csv'
	df = pd.read_csv(csv_file_path)
	books = df.to_dict('records')
	return render(request, 'index.html', {'books': books})

pivot_table = pd.read_csv('data/pivot_table.csv', index_col='Book-Title')
result = pd.read_csv('data/result.csv')
with open('data/similar_items.json', 'r') as f:
	similar_items_dict = json.load(f)

# Ensure index is string type for pivot table
pivot_table.index = pivot_table.index.astype(str)

def get_book_details(book_title, result):
	book_info = result[result['Book_Title'] == book_title]
	if not book_info.empty:
		book_info = book_info.iloc[0]
		return {
			'Book_Title': book_info['Book_Title'],
			'Book_Author': book_info['Book_Author'],
			'Publisher': book_info['Publisher'],
			'num_ratings': book_info['num_ratings'],
			'avg_rating': book_info['avg_rating'],
			'Image_URL_M': book_info['Image_URL_M']
		}
	return {}

def get_recommendations_by_criteria(criteria_value, column_name, exclude_book, result):
	criteria_books = result[result[column_name] == criteria_value]['Book_Title'].tolist()
	criteria_books = [book for book in criteria_books if book != exclude_book]
	return criteria_books[:6]

def recommend_ui(book_name, pt, result, similar_items_dict):
	recommendations = {
		'best_matches': [],
		'similar_books': [],
		'books_by_same_author': [],
		'books_by_same_publisher': []
	}

	if not book_name:
		return recommendations

	# Step 1: Check for partial matches in the pivot table
	best_matches = pt.index[pt.index.str.contains(book_name, case=False, na=False, regex=False)].tolist()
	if best_matches:
		best_match = best_matches[0]

		recommendations['best_matches'] = [get_book_details(title, result) for title in best_matches[:5]]

		recommendations['similar_books'] = [
			get_book_details(title, result)
			for title in similar_items_dict.get(best_match, [])
			if title not in best_matches
		][:8]
	else:
		# Step 2: Check for partial matches in the result DataFrame
		best_matches = result[result['Book_Title'].str.contains(book_name, case=False, na=False, regex=False)]['Book_Title'].unique().tolist()
		close_matches_result = difflib.get_close_matches(book_name, result['Book_Title'], n=1, cutoff=0.6)

		recommendations['best_matches'] = [get_book_details(title, result) for title in best_matches[:5]]
		recommendations['best_matches'] = [get_book_details(title, result) for title in close_matches_result[:5]]

		if close_matches_result:
			best_match_book = close_matches_result[0]
			book_details = result[result['Book_Title'] == best_match_book]
			if not book_details.empty:
				book_details = book_details.iloc[0]
				author = book_details['Book_Author']
				publisher = book_details['Publisher']

				books_by_same_author = get_recommendations_by_criteria(author, 'Book_Author', best_match_book, result)
				books_by_same_publisher = get_recommendations_by_criteria(publisher, 'Publisher', best_match_book, result)

				recommendations['books_by_same_author'] = [get_book_details(book, result) for book in books_by_same_author[:5]]
				recommendations['books_by_same_publisher'] = [get_book_details(book, result) for book in books_by_same_publisher[:5]]

	return recommendations

def recommendation(request):
	query = request.GET.get('q')
	recommendations = recommend_ui(query, pivot_table, result, similar_items_dict)
	return render(request, 'recommendation.html', {'recommendations': recommendations, 'query': query})