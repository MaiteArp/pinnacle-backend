import pytest
from app import create_app
from app import db
from app.models.user import User


@pytest.fixture
def app():
    #create the app with a test config dict
    app = create_app({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield app
    # close and remove the temp database 
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


#  This fixture creates a user and saves it in the DB
@pytest.fixture
def one_user(app):
    new_user = User(name="Bob", password="Ross")
    db.session.add(new_user)
    db.session.commit()

