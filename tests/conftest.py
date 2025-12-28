from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
from app import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.config import settings
from app.database import Base
import pytest
from alembic import command

from app.oauth2 import create_access_token

# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://postgres:123456@localhost:5432/fastapi_test"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"  #"postgresql+psycopg://postgres:123456@localhost:5432/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Testing_Session_local = sessionmaker(bind=engine,autoflush=False,autocommit = False)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_Session_local()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email":"pytest@gmail.com","password":"123456"}

    res = client.post("/users",json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"pytest2@gmail.com","password":"123456"}

    res = client.post("/users",json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token,session):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data = [{
    "title": "first title",
    "content": "first content",
    "owner_id": test_user['id']
    }, {
    "title": "2nd title",
    "content": "2nd content",
    "owner_id": test_user['id']
    }, {
    "title": "3rd title",
    "content": "3rd content",
    "owner_id": test_user['id']
    }, {
        "title": "4rd title",
        "content": "4rd content",
        "owner_id": test_user2['id']
    }

    ]

    posts = [models.Post(**post) for post in posts_data]

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts



@pytest.fixture
def test_vote(test_posts,session,test_user):
    new_vote = models.Vote(post_id= test_posts[3].id,user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
