import pytest
from app import app
# import sqlalchemy

@pytest.fixture(scope="session")
def app():
    app.config.from_object("config.TestingConfig")
    return app

@pytest.fixture()
def client(test_app):
    return test_app.test_client()

# @pytest.fixture()
# def database(test_app):
#     _db.app = test_app
#     with test_app.app_context():
#         _db.create_all()
#
#     yield _db
#
#     _db.session.close()
#     _db.drop_all()