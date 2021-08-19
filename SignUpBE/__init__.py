import logging

import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger function processed a request.The function is SignUpBE.')

    id = req.params.get('id')
    password = req.params.get('password')
    email = req.params.get('email')

    if not id or not password:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            id = req_body.get('id')
            password = req_body.get('password')
            email = req_body.get('email')         

    if not all([id, password,email]):
        logging.info(f"{id},{password},{email}")
        return func.HttpResponse('id or password or email is empty!', status_code=210)
    else:
        url = 'https://ovaas2functiondal.azurewebsites.net/api/createuserdal'
        params = {'id': id, 'password': password, 'email': email}
        logging.info(f"body is {params}")

        response = requests.post(params=params, url=url)
        logging.info(
            f"response.get_body is {response.text},status_code is {response.status_code}")
        if response.status_code == 211:
            return func.HttpResponse(f'[Failed]:The user {id} exists.status_code is 211.', status_code=211)
        elif response.status_code==210:
            logging.info(f'[Failed]:Failed to create user {id}.status_code is 210.')
            return func.HttpResponse(f'[Failed]: Failed to create user {id}.status_code is 210.', status_code=210)
        elif response.status_code == 200:
            return func.HttpResponse(f'[Success]:User {id} created successfully', status_code=200)

# test data is 
#  {"id": "4", "password": "4","email":"mail@gmail.com"}
