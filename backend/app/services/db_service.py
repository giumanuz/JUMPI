import logging

import app.config as config
from app.services.database.database import Database
from app.services.database.elastic import ElasticsearchDb


def setup_db():
    db = ElasticsearchDb(url=config.APP_CONFIG.ELASTIC_URL)
    db.logger.setLevel(logging.DEBUG if config.APP_CONFIG.DEBUG else logging.INFO)
    Database.set_instance(db)
