from unittest.mock import patch

import pytest

from dao.model.genre import Genre
from service.genre import GenreService
from dao.genre import GenreDAO


class TestGenreService:

    @pytest.fixture()
    @patch('dao.genre.GenreDAO')
    def genre_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_one.return_value = Genre(id=1, name='test_genre')
        dao.get_all.return_value = [
            Genre(id=1, name='test_genre_1'),
            Genre(id=2, name='test_genre_2'),
        ]
        dao.create.return_value = Genre(id=1, name='test_genre')
        dao.update.return_value = Genre(id=1, name='updated_genre')
        dao.delete.return_value = None
        return dao

    @pytest.fixture()
    def genre_service(self, genre_dao_mock):
        return GenreService(dao=genre_dao_mock)

    @pytest.fixture
    def genre(self, db):
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_genre(self, genre_service, genre):
        assert genre_service.get_one(genre.id)

    def test_genre_get_all(self, genre_service):
        assert len(genre_service.get_all()) == 2

    def test_genre_create(self, genre_service, genre_as_dict):
        assert genre_service.create(genre_as_dict).name == 'test_genre'

    def test_genre_update(self, genre_service, genre_as_dict):
        assert genre_service.update(genre_as_dict).name == 'updated_genre'

    def test_genre_part_update(self, genre_service, genre_dao_mock, genre_as_dict):
        genre_service.partially_update(genre_as_dict)
        assert genre_dao_mock.update.called

    def test_genre_delete(self, genre_service, genre_dao_mock):
        genre_service.delete(1)
        assert genre_dao_mock.delete.called

