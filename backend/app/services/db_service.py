import logging
import os

from database_utils.database import Database
from database_utils.elastic import ElasticsearchDb


def setup_db(debug=False):
    elastic_url = os.getenv('ELASTIC_URL')
    db = ElasticsearchDb(url=elastic_url)
    db.logger.setLevel(logging.DEBUG if debug else logging.INFO)
    Database.set_instance(db)
