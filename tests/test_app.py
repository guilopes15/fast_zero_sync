from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'testusername', 'email': 'test@test.com'}
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'testusername2',
            'email': 'test@test.com',
            'password': '123',
        },
    )
    assert response.json() == {
        'id': 1,
        'username': 'testusername2',
        'email': 'test@test.com',
    }


def test_update_user_with_invalid_id(client):
    response = client.put(
        '/users/2',
        json={
            'id': 2,
            'username': 'testusername3',
            'email': 'test@test.com',
            'password': '123',
        },
    )
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_with_invalid_id(client):
    response = client.delete('/users/2')
    assert response.json() == {'detail': 'User not found'}
