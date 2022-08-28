from unittest.mock import patch

import pytest

from dao.model.director import Director
from service.director import DirectorService
from dao.director import DirectorDAO


class TestDirectorService:

    @pytest.fixture()
    @patch('dao.director.DirectorDAO')
    def director_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_one.return_value = Director(id=1, name='test_director')
        dao.get_all.return_value = [
            Director(id=1, name='test_director_1'),
            Director(id=2, name='test_director_2'),
        ]
        dao.create.return_value = Director(id=1, name='test_director')
        dao.update.return_value = Director(id=1, name='updated_director')
        dao.delete.return_value = None
        return dao

    @pytest.fixture()
    def director_service(self, director_dao_mock):
        return DirectorService(dao=director_dao_mock)

    @pytest.fixture
    def director(self, db):
        obj = Director(name="director")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_director(self, director_service, director):
        assert director_service.get_one(director.id)

    def test_director_get_all(self, director_service):
        assert len(director_service.get_all()) == 2

    def test_director_create(self, director_service, director_as_dict):
        assert director_service.create(director_as_dict).name == 'test_director'

    def test_director_update(self, director_service, director_as_dict):
        assert director_service.update(director_as_dict).name == 'updated_director'

    def test_director_part_update(self, director_service, director_dao_mock, director_as_dict):
        director_service.partially_update(director_as_dict)
        assert director_dao_mock.update.called

    def test_director_delete(self, director_service, director_dao_mock):
        director_service.delete(1)
        assert director_dao_mock.delete.called

