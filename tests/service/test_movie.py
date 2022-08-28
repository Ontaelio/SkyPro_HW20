from unittest.mock import patch

import pytest

from dao.model.movie import Movie
from service.movie import MovieService
from dao.movie import MovieDAO


class TestMovieService:

    @pytest.fixture()
    @patch('dao.movie.MovieDAO')
    def movie_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao = dao_mock()
        dao.get_one.return_value = Movie(id=1,
                                         title='test_movie',
                                         description='1234',
                                         trailer='link',
                                         year=1999,
                                         rating=7.0,
                                         genre_id=1,
                                         director_id=1
                                         )
        dao.get_all.return_value = [
            Movie(id=1,
                  title='test_movie',
                  description='1234',
                  trailer='link',
                  year=1999,
                  rating=7.0,
                  genre_id=1,
                  director_id=1
                  ),

            Movie(id=2,
                  title='test_movie2',
                  description='1234',
                  trailer='link',
                  year=2009,
                  rating=7.1,
                  genre_id=1,
                  director_id=1
                  ),
        ]
        dao.create.return_value = Movie(id=1, title='test_movie')
        dao.update.return_value = Movie(id=1, title='updated_movie')
        dao.delete.return_value = None
        return dao

    @pytest.fixture()
    def movie_service(self, movie_dao_mock):
        return MovieService(dao=movie_dao_mock)

    @pytest.fixture
    def movie(self, db):
        obj = Movie(title="movie",
                    description='1234',
                    trailer='link',
                    year=1999,
                    rating=7.0,
                    genre_id=1,
                    director_id=1
                    )
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_movie(self, movie_service, movie):
        assert movie_service.get_one(movie.id)

    def test_movie_get_all(self, movie_service):
        assert len(movie_service.get_all()) == 2

    def test_movie_create(self, movie_service, movie_as_dict):
        assert movie_service.create(movie_as_dict).title == 'test_movie'

    def test_movie_update(self, movie_service, movie_as_dict):
        movie_as_dict['id'] = 1
        assert movie_service.update(movie_as_dict).title == 'updated_movie'

    def test_movie_part_update(self, movie_service, movie_dao_mock, movie_as_dict):
        movie_as_dict['id'] = 1
        movie_service.partially_update(movie_as_dict)
        assert movie_dao_mock.update.called

    def test_movie_delete(self, movie_service, movie_dao_mock):
        movie_service.delete(1)
        assert movie_dao_mock.delete.called

