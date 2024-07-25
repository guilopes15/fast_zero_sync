from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode, encode

from fast_zero.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_current_user,
)


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        'users/1',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not_found(token, session):
    data = {'sub': 'None@none.com'}
    token = encode(data, SECRET_KEY, algorithm=ALGORITHM)
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'www-Authenticate': 'Bearer'},
    )

    with pytest.raises(HTTPException) as ex:
        get_current_user(session, token=token)

    assert ex.value.detail == credentials_exception.detail
