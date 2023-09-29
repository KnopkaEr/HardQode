import requests
from requests.auth import HTTPBasicAuth
import URLS
import data

basic = HTTPBasicAuth(data.username, data.password)


def get_category(params=None):
    if params is None:
        params = {}
    return requests.get(URLS.URL_PROJECT + URLS.URL_CATEGORY, headers=data.headers_api, auth=basic, params=params)


def post_category(body=None):
    if body is None:
        body = {}
    return requests.post(URLS.URL_PROJECT + URLS.URL_CATEGORY, headers=data.headers_api, auth=basic, json=body)


def get_category_id(id_cat=None):
    if id_cat is not None:
        id_cat = str(id_cat) + "/"
        return requests.get(URLS.URL_PROJECT + URLS.URL_CATEGORY + id_cat, headers=data.headers_api, auth=basic)
    else:
        return requests.get(URLS.URL_PROJECT + URLS.URL_CATEGORY, headers=data.headers_api, auth=basic)


def put_category_id(id_cat=None, body=None):
    if body is None:
        body = {}
    if id_cat is None:
        id_cat = ''
    else:
        id_cat = str(id_cat) + "/"
    return requests.put(URLS.URL_PROJECT + URLS.URL_CATEGORY + id_cat, headers=data.headers_api, auth=basic, json=body)


def delete_category_id(id_cat=None):
    if id_cat == None:
        id_cat = ''
    else:
        id_cat = str(id_cat) + "/"
    return requests.delete(URLS.URL_PROJECT + URLS.URL_CATEGORY + id_cat, headers=data.headers_api, auth=basic)



def get_pet(params=None):
    if params is None:
        params = {}
    return requests.get(URLS.URL_PROJECT + URLS.URL_PET, headers=data.headers_api, auth=basic, params=params)


def post_pet(body=None):
    if body is None:
        body = {}
    return requests.post(URLS.URL_PROJECT + URLS.URL_PET, headers=data.headers_api, auth=basic, json=body)


def get_pet_id(id_pet=None):
    if id_pet is None:
        id_pet = ''
    else:
        id_pet = str(id_pet) + "/"
    return requests.get(URLS.URL_PROJECT + URLS.URL_PET + id_pet, headers=data.headers_api, auth=basic)


def put_pet_id(id_pet=None, body=None):
    if body is None:
        body = {}
    if id_pet is None:
        id_pet = ''
    else:
        id_pet = str(id_pet) + "/"
    return requests.put(URLS.URL_PROJECT + URLS.URL_PET + id_pet, headers=data.headers_api, auth=basic, json=body)


def delete_pet_id(id_pet=None):
    if id_pet is None:
        id_pet = ''
    else:
        id_pet = str(id_pet) + "/"
    return requests.delete(URLS.URL_PROJECT + URLS.URL_PET + id_pet, headers=data.headers_api, auth=basic)


def post_token_auth(body=None):
    if body is None:
        body = {}
    return requests.post(URLS.URL_PROJECT + URLS.URL_TOKEN, headers=data.headers_api, json=body)
