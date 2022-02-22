from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

# config
config = {
    'cloud_ID': 'Karan:ZXUtd2VzdC0xLmF3cy5mb3VuZC5pbyRjOTk1NzUwMWQ3ODQ0M2RjOTQ2NjY4YTllNzQzNWI0MCQ4M2ViMDIwMTVmNDQ0YmJiOGM3OTYyMjMxZDhkNDNkMQ==',
    'username': 'elastic',
    'password': 'bUnEKgI2TGHeOxp7AXB9SXh0'
}

# Check for Connection
es = Elasticsearch(cloud_id=config['cloud_ID'], http_auth=(
    config['username'], config['password']))
if es.ping():
    print('Elasticsearch connected.')
else:
    print('Elasticsearch not connected.')


books = pd.read_csv(
"https://raw.githubusercontent.com/Rmanjeet/Simple-Book-Recommendation-System/main/books.csv")

Vectorizer = TfidfVectorizer(ngram_range=(1, 2))
Vectorizer.fit(books['features'])

Vec = Vectorizer.transform(books['features'])

def similar(book_name):
    book_vec = Vectorizer.transform([book_name])
    sim = cosine_similarity(book_vec, Vec)
    result = sim[0]

    # Get the indexes/indices of elements greater than 4 
    mask = np.where(result >= 0.03)[0]
    score_index = {}
    for index in mask:
        score_index[index]=result[index]

    indexes = [index[0] for index in sorted(score_index.items(), key=lambda item: item[1])]
    indexes = list(reversed(indexes))
    result = []
    for i in indexes:
        result.append({
        'title' : books.Title[i],
        'author' : books.Author[i],
        'publisher' : books.Publisher[i],
        'img' : books.Image[i],
        }
        )
    return result

# check for indices
if 'test' in es.indices.get_alias():
    print("'test' index is present.")
else:
    # Define Structure of Index
    b = {"mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "author": {
                "type": "text"
            },
            "publisher": {
                "type": "text"
            },
            "img": {
                "type": "text"
            }
        }
    }
    }
    # 400 caused by IndexAlreadyExistsException,
    ret = es.indices.create(index='books', ignore=400, body=b)
    print("* 'test' index is structured.")

    # Read Store Data
    for index, row in books.iterrows():
        title = row[0]
        author = row[1]
        publisher = row[4]
        img = row[6]
        b = {"title": title,
            "author": author,
            "publisher": publisher,
            "img": img
            }
        es.index(index="test", id=index, document=b)
        if index % 100 == 0:
            print(index, ' record indexed.')
    print("* 'test' indexing completed.")


# Keyword based search
def keywordSearch(es, q):
    # Search by Keywords
    b = {
        'match': {
            "title": q
        }
    }
    res = es.search(index='test', query=b)
    return res['hits']['hits']
