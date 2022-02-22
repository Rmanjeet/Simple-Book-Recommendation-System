from flask import Flask, request, render_template
import pandas as pd
from utilsES import *

app = Flask(__name__)

books = pd.read_csv('https://raw.githubusercontent.com/Rmanjeet/Simple-Book-Recommendation-System/main/books.csv')

# Rendering home page
@app.route("/")
def hello_world():
    home_display = books.to_dict('r')
    return render_template('index.html', home_display_books=home_display)

# Rendering Selected book
@app.route("/Read/<keyword>")
def read(keyword):
    similarity = similar(keyword)
    return render_template('read.html', similarity=similarity)

# Rendering search keyword
@app.route('/Search', methods=['GET', 'POST'])
def search():
    query = request.form['search_text']
    search_dict = keywordSearch(es, query)
    return render_template('search.html', search_dict = search_dict, book=query)

if __name__ == '__main__':
    app.run(debug=True)