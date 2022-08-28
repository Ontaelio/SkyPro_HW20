import pytest

from config import TestConfig
from app import create_app
from setup_db import db as database


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


# @pytest.fixture
# def request_context():
#     app = create_app(TestConfig)
#     return app.test_request_context


@pytest.fixture
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def director_as_dict():
    return {'id': 1,
            'name': 'Ослик Натужный'}

@pytest.fixture
def genre_as_dict():
    return {'id': 1,
            'name': 'Внезапность'}


@pytest.fixture
def movie_as_dict():
    return {
            'title': 'Test movie',
            'description': 'Test arrives at Testtown, then test happens',
            'trailer': 'youtube',
            'year': 1998,
            'rating': 9.0,
            'genre_id': 1,
            'director_id': 1,
            }
