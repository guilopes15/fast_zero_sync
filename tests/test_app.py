from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange(organização)
    response = client.get('/')  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # Assert (afirmação)
    assert response.json() == {'message': 'Ola mundo'}


def test_ola_mundo_deve_retornar_ok_e_htmlresponse():
    client = TestClient(app)
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
