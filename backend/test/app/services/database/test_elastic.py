import pytest
from unittest.mock import MagicMock
from app.services.database.elastic import ElasticsearchDb, Magazine, Article, MagazineNotFoundError, MagazineExistsError
from app import create_app

@pytest.fixture
def es_db(mocker):
    """Fixture to create an instance of ElasticsearchDb with application context."""
    
    app = create_app()  # Crea la tua app Flask
    with app.app_context():
        # Crea un'istanza di ElasticsearchDb
        es_db = ElasticsearchDb(url="http://localhost:9200")
        
        # Mock della proprietà 'es'
        mock_es = MagicMock()  # Crea un mock del client Elasticsearch
        
        # Patch della proprietà 'es' per restituire un oggetto MagicMock
        mocker.patch.object(ElasticsearchDb, 'es', mock_es)  # Mock della proprietà 'es'
        
        yield es_db


def test_ping(es_db):
    """Test del metodo ping di ElasticsearchDb."""
    es_db.es.ping.return_value = True  # Mock della risposta positiva
    assert es_db.ping() is True  # Verifica che ping() restituisca True

    es_db.es.ping.return_value = False  # Mock della risposta negativa
    assert es_db.ping() is False  # Verifica che ping() restituisca False


# def test_add_magazine(es_db):
#     """Test che aggiunge una rivista con successo."""
    
#     # Mock della risposta di ricerca, indicando che la rivista non esiste
#     search_mock = MagicMock()
#     search_mock.body = {'hits': {'total': {'value': 0}, 'hits': []}}  # Simula che la rivista non esiste
#     es_db.es.search.return_value = search_mock
    
#     # Mock della risposta di creazione del documento Elasticsearch
#     index_mock = MagicMock()
#     index_mock.body = {'_id': '12345', 'result': 'created'}  # Risposta mock di successo
#     es_db.es.index.return_value = index_mock
    
#     # Mock del metodo magazine_exists per evitare che sollevi l'errore MagazineExistsError
#     es_db.magazine_exists = MagicMock(return_value=False)
    
#     # Creazione di un oggetto Magazine
#     magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    
#     # Aggiungi la rivista e verifica che l'ID restituito sia quello giusto
#     magazine_id = es_db.add_magazine(magazine)
    
#     # Verifica che l'ID restituito sia '12345'
#     assert magazine_id == '12345'
    
#     # Verifica che la funzione es.index sia stata chiamata correttamente
#     es_db.es.index.assert_called_once_with(index='magazines', document=vars(magazine))
    
#     # Assicuriamoci che il mock del risultato di indicizzazione restituisca il body giusto
#     assert index_mock.body['_id'] == '12345'  # Verifica che _id sia quello corretto

# def test_add_magazine_exists(es_db):
#     """Test che solleva un'eccezione se la rivista esiste già."""
#     # Mock della risposta di ricerca per simulare una rivista esistente
#     es_db.es.search.return_value = {'hits': {'total': {'value': 1}, 'hits': [{' _id': '12345'}]}}
    
#     magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    
#     with pytest.raises(MagazineExistsError):  # Verifica che venga sollevata l'eccezione
#         es_db.add_magazine(magazine)


# def test_add_article_to_existing_magazine(es_db):
#     """Test che un articolo venga aggiunto con successo ad una rivista esistente."""
#     # Mock della risposta di recupero dell'ID della rivista
#     es_db.get_magazine_id = MagicMock(return_value='12345')
    
#     # Mock della risposta di aggiornamento Elasticsearch
#     es_db.es.update.return_value = {'_id': '12345', 'result': 'updated'}
    
#     # Creazione di un articolo con il parametro page_offsets
#     article = Article(title="AI Innovations", author="John Doe", content="Content of the article.", page_offsets=[])
#     magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    
#     result = es_db.add_article(magazine, article)
    
#     assert result == {'_id': '12345', 'result': 'updated'}  # Verifica il risultato


# def test_get_magazine_id(es_db):
#     """Test che recupera correttamente l'ID della rivista."""
#     # Mock della risposta di ricerca di Elasticsearch
#     es_db.es.search.return_value = {
#         'hits': {
#             'total': {'value': 1},
#             'hits': [{' _id': '12345'}]
#         }
#     }
    
#     magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
    
#     magazine_id = es_db.get_magazine_id(magazine)
    
#     assert magazine_id == '12345'  # Verifica che l'ID della rivista sia quello giusto


# def test_magazine_not_found_error(es_db):
#     """Test che solleva un'eccezione quando la rivista non viene trovata."""
#     # Mock della risposta di ricerca che simula una rivista non trovata
#     es_db.es.search.return_value = {'hits': {'total': {'value': 0}, 'hits': []}}
    
#     magazine = Magazine(name="Non Existent Magazine", year=2024, publisher="Unknown Publisher")
    
#     with pytest.raises(MagazineNotFoundError):  # Verifica che venga sollevata l'eccezione
#         es_db.get_magazine_id(magazine)


# def test_query(es_db):
#     """Test che esegue una query complessa e verifica la risposta."""
#     # Mock della risposta di ricerca di Elasticsearch
#     es_db.es.search.return_value = {
#         'hits': {
#             'total': {'value': 1},
#             'hits': [{' _id': '12345', '_source': {'name': 'Tech Monthly'}}]
#         }
#     }
    
#     magazine = Magazine(name="Tech Monthly", year=2024, publisher="Tech Publisher")
#     article = Article(title="AI Innovations", author="John Doe", content="Content of the article.", page_offsets=[])
    
#     response = es_db.query(magazine, article)
    
#     assert response['hits']['hits'][0]['_id'] == '12345'  # Verifica la risposta
