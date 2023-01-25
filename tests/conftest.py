import pytest


@pytest.fixture
def test_data():
    return {
        'test': 'test'
    }


def client():
    from app import app
    return app.test_client()
