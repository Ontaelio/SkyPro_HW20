from config import TestConfig
from app import create_app


class TestConfiguration:

    def test_testing(self):
        app_config = create_app(TestConfig).config
        assert app_config["TESTING"] is True
        assert app_config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"