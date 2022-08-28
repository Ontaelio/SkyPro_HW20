from time import sleep

import pytest

from dao.model.director import Director
from dao.model.genre import Genre
from dao.movie import MovieDAO
from dao.model.movie import Movie


class TestMoviesDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MovieDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(title="Фильм 1",
                  description="Трам парам пам пам, старый немой боевик.",
                  trailer="https://www.youtube.com/watch?v=BB61nauFkds",
                  year=1902,
                  rating=3.4,
                  genre_id=1,
                  director_id=1, )
        d = Director(name="Зайчик Крошечный")
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.add(d)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(title="Фильм 2",
                  description="Тут все очень интересно и увлекательно.",
                  trailer="https://www.youtube.com/watch?v=BB61nauFkds",
                  year=2025,
                  rating=9.4,
                  genre_id=2,
                  director_id=2, )
        d = Director(name="Котик Крупноватый")
        g = Genre(name="Комедия")
        db.session.add(g)
        db.session.add(d)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_one(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_one(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_create(self, movies_dao, movie_1, movie_as_dict):
        movies_dao.create(movie_as_dict)
        a = movies_dao.get_one(2)
        assert a.title == movie_as_dict['title']
        assert a.description == movie_as_dict['description']
        assert a.trailer == movie_as_dict['trailer']
        assert a.year == movie_as_dict['year']
        assert a.rating == movie_as_dict['rating']
        assert a.genre_id == movie_as_dict['genre_id']
        assert a.director_id == movie_as_dict['director_id']

    def test_update(self, movies_dao, movie_1, movie_as_dict):
        assert movies_dao.get_one(movie_1.id) == movie_1
        movie_as_dict['id'] = 1
        movies_dao.update(movie_as_dict)
        a = movies_dao.get_one(movie_1.id)
        assert a.title == movie_as_dict['title']
        assert a.description == movie_as_dict['description']
        assert a.trailer == movie_as_dict['trailer']
        assert a.year == movie_as_dict['year']
        assert a.rating == movie_as_dict['rating']
        assert a.genre_id == movie_as_dict['genre_id']
        assert a.director_id == movie_as_dict['director_id']

    def test_delete(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_one(movie_2.id) == movie_2
        movies_dao.delete(movie_2.id)
        assert movies_dao.get_one(movie_2.id) is None
