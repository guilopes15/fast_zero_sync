from http import HTTPStatus
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Ola mundo'}
