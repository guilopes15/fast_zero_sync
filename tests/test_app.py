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
