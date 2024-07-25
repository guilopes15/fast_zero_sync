from http import HTTPStatus

from sqlalchemy import select

from fast_zero.models import User
from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # Assert (afirmação)
    assert response.json() == {'message': 'Ola mundo'}


def test_ola_mundo_deve_retornar_ok_e_htmlresponse(client):
    response = client.get('/ex')

    html = """
    <html>
      <head>
        <title>Olá Mundo</title>
      </head>
      <body>
        <h1>Olá Mundo</h1>
      </body>
    </html>"""

    assert response.status_code == HTTPStatus.OK
    assert response.text == html


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    # Valida o UserPublic
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_create_user_with_username_already_existent(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test2@test.com',
            'password': 'password',
        },
    )
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_email_already_existent(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test2',
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    # convertendo o user do sqlalchemy para o UserPublic do pydantic
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, session, user):
    response = client.get('/users/1')
    user_id = 1
    db_user = session.scalar(select(User).where(User.id == user_id))
    session.refresh(db_user)
    db_user = UserPublic.model_validate(db_user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == db_user


def test_read_user_by_id_with_invalid_id(client, fake_user):
    response = client.get('/users/2')
    assert fake_user is None
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': user.id,
            'username': 'testusername2',
            'email': 'test@test.com',
            'password': '123',
        },
    )
    assert response.json() == {
        'id': user.id,
        'username': 'testusername2',
        'email': 'test@test.com',
    }


def test_update_user_with_invalid_id(client, fake_user):
    response = client.put(
        '/users/2',
        json={
            'id': 2,
            'username': 'testusername3',
            'email': 'test@test.com',
            'password': '123',
        },
    )
    assert fake_user is None
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_with_invalid_id(client, fake_user):
    response = client.delete('/users/2')
    assert fake_user is None
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
