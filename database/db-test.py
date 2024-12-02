from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from os import environ

load_dotenv()

es = Elasticsearch(
    ["https://jumpi.edotm.net/elastic"],
    api_key=environ.get("ELASTIC_API_KEY"),
)

if es.ping():
    print("Successfully connected to Elasticsearch!")
else:
    print("Connection failed.")

# Define the search criteria for the magazine
magazine_name = "Casabella continuità"
magazine_year = 1965
magazine_publisher = "Milano : Domus"

# Define the new article to add
new_article = {
    "title": "I SOLITI FARISEI 2",
    "author": "Ernesto N. Rogers",
    "content": "The content of the article...",
    "images": [
        {
            "caption": "Figura 2",
            "page": 4
        }
    ],
    "page_range": [3, 24],
    "page_offsets": [12412, 23142]
}

# Define the magazine document template to create if not found
magazine_template = {
    "name": magazine_name,
    "abstract": "Rivista internazionale di architettura.",
    "year": magazine_year,
    "publisher": magazine_publisher,
    "genre": "Periodical",
    "articles": []  # Initialize with an empty list of articles
}

# 1. Search for the magazine
search_query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"name": magazine_name}},
                {"range": {"year": {
                    "gte": magazine_year,
                    "lte": magazine_year
                }}},
                {"term": {"publisher": magazine_publisher}}
            ]
        }
    },
    "fields": ["_id"],
    "_source": False
}

try:
    # Perform the search query to find the magazine
    search_response = es.search(index="magazines", body=search_query)

    # If no hits found, create the magazine
    if search_response['hits']['total']['value'] == 0:
        print(f"Magazine '{magazine_name}' not found. Creating it...")

        # Create a new magazine document
        create_response = es.index(index="magazines", document=magazine_template)
        magazine_id = create_response['_id']
        print(f"Magazine created with ID: {magazine_id}")
    else:
        # Magazine found, retrieve its ID
        magazine_id = search_response['hits']['hits'][0]['_id']
        print(f"Found magazine '{magazine_name}' with ID: {magazine_id}")
except Exception as e:
    print(f"Error searching for the magazine: {e}")

# 2. Update the magazine by adding a new article
exit(0)
try:
    update_response = es.update(
        index="magazines",  # The index where your magazine document is stored
        id=magazine_id,  # The ID of the magazine document to update
        body={
            "script": {
                "source": "ctx._source.articles.add(params.new_article);",
                "params": {
                    "new_article": new_article  # The article to add to the magazine
                }
            }
        }
    )
    print(f"Article added to magazine with ID {magazine_id}: {update_response}")
except Exception as e:
    print(f"Error updating the magazine with article: {e}")