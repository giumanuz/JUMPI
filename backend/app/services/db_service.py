import logging
import os

from app.config import APP_CONFIG
from app.services.database.database import Database
from app.services.database.elastic import ElasticsearchDb


def setup_db():
    db = ElasticsearchDb(url=APP_CONFIG.ELASTIC_URL)
    db.logger.setLevel(logging.DEBUG if APP_CONFIG.DEBUG else logging.INFO)
    Database.set_instance(db)
