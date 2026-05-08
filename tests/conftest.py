import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings as sc
from src.database import Base, get_db
from src.main import app

engine = create_engine(sc.DB_URL)
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal()

    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client: TestClient):
    test_user = {"name": "test_user", "password": "secureTestPassword"}
    client.post("/register", json=test_user)

    # token provider
    response = client.post("/login", json=test_user)
    token = response.json()["token"]
    yield token

    # cleanup
    client.delete(f"/users/{test_user['name']}")


TEST_USER = {"name": "test_user", "password": "secureTestPassword"}


def AUTH_HEADER(token):
    return {"Authorization": f"Bearer {token}"}
