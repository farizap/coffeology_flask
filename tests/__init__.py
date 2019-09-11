import pytest
import json
import logging
from flask import Flask, request, json
from blueprints import app, db
from app import cache
from blueprints.method.model import Methods
from blueprints.recipe.model import Recipes
from blueprints.user.model import Users
from blueprints.step.model import Steps


def call_client(request):
    client = app.test_client()
    return client


@pytest.fixture
def client(request):
    return call_client(request)


def reset_database():

    db.drop_all()
    db.create_all()

    method = Methods("name", "icon", 1)
    recipe = Recipes(1, "name", 1, 1, "beanName",
                     "beanProcess", "beanRoasting", 1, 1, 1)
    user = Users("email@email.com", "password", "name", 1, 1, "photo", 1, 1)
    step = Steps(1, 1, 1, "note", 1, 1)

    # save users to database
    db.session.add(method)
    db.session.add(recipe)
    db.session.add(user)
    db.session.add(step)
    db.session.commit()


def create_token_non_internal():
    pass
    # token = cache.get('token-non-internal')
    # if token is None:
    #     ## prepare request input
    #     data = {
    #         'username': 'tes',
    #         'password': 'tes'
    #     }

    #     ## do request
    #     req = call_client(request)
    #     res = req.post('/token', data=json.dumps(data),
    #                    content_type='application/json')

    # # store response
    #     res_json = json.loads(res.data)

    #     logging.warning('RESULT : %s', res_json)

    #     ## assert / compare with expected result
    #     assert res.status_code == 200

    #     ## save token into cache
    #     cache.set('token-non-internal', res_json['token'], timeout=60)

    #     ## return because it useful for other test
    #     return res_json['token']
    # else:
    #     return token


def create_token_internal():
    pass
    # token = cache.get('token-internal')
    # if token is None:
    #     ## prepare request input
    #     data = {
    #         'username': 'tes',
    #         'password': 'tes',
    #         'email' : 'tes@tes.com'
    #     }

    #     ## do request
    #     req = call_client(request)
    #     res = req.post('/token/admin', data=json.dumps(data),
    #                    content_type='application/json')
    #     ## store response
    #     res_json = json.loads(res.data)

    #     logging.warning('RESULT : %s', res_json)

    #     ## assert / compare with expected result
    #     assert res.status_code == 200

    #     ## save token into cache
    #     cache.set('token-internal', res_json['token'], timeout=60)

    #     ## return because it useful for other test
    #     return res_json['token']
    # else:
    #     return token
