import logging

import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger function processed a request.The function is LoginBE.')

    id = req.params.get('id')
    password = req.params.get('password')

    if not id or not password:
        try:
            req_body = req.get_json()
        except ValueError as e:
            logging.info(f"[Error]:{e}")
        else:
            id = req_body.get('id')
            password = req_body.get('password')

    if not all([id, password]):
        logging.info(f"id or password is empty!")
        return func.HttpResponse('id or password is empty!', status_code=210)

    if id and password:
        url = 'https://ovaas2functiondal.azurewebsites.net/api/logindal'
        params = {'id': id, 'password': password}
        logging.info(f"params is {params}")

        response = requests.post(url=url, params=params)
        logging.info(
            f"response.get_body is {response.text},status_code is {response.status_code}")
        if response.status_code == 211:
            logging.info(f'[Failed]:status_code is 211')
            return func.HttpResponse(f'[Failed]:status_code is 211', status_code=211)
        elif response.status_code==200:
            return func.HttpResponse('[Success]:The user exists. The id and password are correct. You can log in.', status_code=200)

# {"id": "1", "password": "123"}
