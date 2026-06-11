import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_health(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'ok'


def test_create_note(client):
    res = client.post('/api/notes', json={
        'title': 'Test note',
        'content': 'This is a test'
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['title'] == 'Test note'


def test_get_notes(client):
    client.post('/api/notes', json={
        'title': 'Note 1',
        'content': 'Content 1'
    })
    res = client.get('/api/notes')
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_create_note_missing_fields(client):
    res = client.post('/api/notes', json={'title': 'only title'})
    assert res.status_code == 400


def test_delete_note(client):
    res = client.post('/api/notes', json={
        'title': 'To delete',
        'content': 'bye'
    })
    note_id = res.get_json()['id']
    res = client.delete(f'/api/notes/{note_id}')
    assert res.status_code == 200
