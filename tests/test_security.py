from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode, encode

from fast_zero.security import create_access_token, get_current_user, settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)
    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
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
    token = encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    with pytest.raises(HTTPException) as ex:
        get_current_user(session, token)

    assert ex.value.status_code == HTTPStatus.UNAUTHORIZED
    assert ex.value.detail == 'Could not validate credentials'


def test_get_current_user_with_invalid_payload(token, session):
    data = {'test': None}
    token = encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    with pytest.raises(HTTPException) as ex:
        get_current_user(session, token)

    assert ex.value.status_code == HTTPStatus.UNAUTHORIZED
    assert ex.value.detail == 'Could not validate credentials'
