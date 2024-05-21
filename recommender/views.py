from django.shortcuts import render
import pandas as pd

# Create your views here.
def index(request):
    csv_file_path = 'data/popular_books.csv'
    df = pd.read_csv(csv_file_path)
    books = df.to_dict('records')
    # Print to console for debugging
    print(books)
    return render(request, 'index.html', {'books': books})