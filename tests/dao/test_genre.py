from time import sleep

import pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre


class TestGenresDAO:

    @pytest.fixture
    def genres_dao(self, db):
        return GenreDAO(db.session)

    @pytest.fixture
    def genre_1(self, db):
        d = Genre(name="Комедия")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def genre_2(self, db):
        d = Genre(name="Боевик")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def genre_last(self, db):
        d = Genre(name="Артхаус")
        sleep(1)
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_genre_by_id(self, genre_1, genres_dao):
        assert genres_dao.get_one(genre_1.id) == genre_1

    def test_get_genre_by_id_not_found(self, genres_dao, genre_1):
        assert genres_dao.get_one(2) is None

    def test_get_all_genres(self, genres_dao, genre_1, genre_2):
        assert genres_dao.get_all() == [genre_1, genre_2]

    def test_create(self, genres_dao, genre_1, genre_as_dict):
        genres_dao.create({'name': genre_as_dict['name']})
        assert genres_dao.get_one(2).name == genre_as_dict['name']

    def test_update(self, genres_dao, genre_1, genre_as_dict):
        assert genres_dao.get_one(genre_1.id) == genre_1
        genres_dao.update(genre_as_dict)
        a = genres_dao.get_one(genre_1.id)
        assert a.name == genre_as_dict['name']

    def test_delete(self, genres_dao, genre_1, genre_2, genre_last):
        assert genres_dao.get_one(genre_last.id) == genre_last
        genres_dao.delete(genre_last.id)
        assert genres_dao.get_one(genre_last.id) is None
