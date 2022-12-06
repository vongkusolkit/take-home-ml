import pytest
import json
from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_points(client):
    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "(3, 10)", "corner_points": "[(1, 1), (3, 1), (1, 3), (3, 3)]"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "(10, 12)", "corner_points": "[(1.5, 1.5), (4.0, 1.5), (1.5, 8.0), "
                                                                            "(4.0, 8.0)]"})
    assert response.status_code == 200

    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "(3, 3)", "corner_points": "[(-1, 1), (1, -1), (-1, 1), (1, -1)]"})
    assert response.status_code == 200


def test_get_points_error(client):
    # Invalid dimensions test
    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "(3, 0)", "corner_points": "[(1, 1), (3, 1), (1, 3), (3, 3)]"})
    assert response.status_code == 400

    # Invalid body test
    response = client.post('http://127.0.0.1:5000/points',
                           json={"d": "(3, 3)", "corner_points": "[(1, 1), (3, 1), (1, 3), (3, 3)]"})
    assert response.status_code == 400

    # Invalid corner points data
    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "(3, 3)", "corner_points": "[(1, 1), (3, 1), (1, 3)]"})
    assert response.status_code == 400

    # Invalid corner points data, coordinates not in a list
    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "(3, 3)", "corner_points": "(1, 1), (3, 1), (1, 3), (3, 3)"})
    assert response.status_code == 400

    # Invalid input test
    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "", "corner_points": ""})
    assert response.status_code == 400

    # Invalid dimensions, has negative
    response = client.post('http://127.0.0.1:5000/points',
                           json={"dimensions": "(-3, 3)", "corner_points": "[(1, 1), (3, 1), (1, 3), (3, 3)]"})
    assert response.status_code == 400



