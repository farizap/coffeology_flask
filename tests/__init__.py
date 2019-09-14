import pytest
import json
import logging
import hashlib
from flask import Flask, request, json
from blueprints import app, db
from app import cache
from blueprints.method.model import Methods
from blueprints.recipe.model import Recipes
from blueprints.recipeDetail.model import RecipeDetails
from blueprints.user.model import Users
from blueprints.step.model import Steps
from blueprints.history.model import History


def callClient(request):
    client = app.test_client()
    return client


@pytest.fixture
def client(request):
    return callClient(request)


def resetDatabase():

    db.drop_all()
    db.create_all()

    passwordHashed = hashlib.md5("Password1".encode()).hexdigest()

    method = Methods("name", "icon", 1)
    recipe = Recipes(1, "name", 1, 1, "beanName", "beanProcess",
                     "beanRoasting", 1, 1, 1, 1)
    user = Users("user@user.com", passwordHashed, "name", "photo")
    user2 = Users("user2@user.com", passwordHashed, "name", "photo")
    admin = Users("admin@admin.com", passwordHashed, "name", "photo")
    step = Steps(1, 1, 1, "note", 1, 1)
    recipeDetail = RecipeDetails(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "note", 2,
                                 92)
    history = History(1, 1)

    # save users to database
    db.session.add(method)
    db.session.add(recipe)
    db.session.add(recipeDetail)
    db.session.add(user)
    db.session.add(user2)
    db.session.add(admin)
    admin.role = 1
    db.session.add(step)
    db.session.add(history)
    db.session.commit()


def createTokenNonInternal():
    token = cache.get('token-non-internal')
    if token is None:
        # prepare request input
        data = {'email': 'user2@user.com', 'password': 'Password1'}

        # do request
        req = callClient(request)
        res = req.post('/token',
                       data=json.dumps(data),
                       content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 200

        # save token into cache
        cache.set('token-non-internal', res_json['token'], timeout=60)

        # return because it useful for other test
        return res_json['token']
    else:
        return token


def createTokenInternal():
    token = cache.get('token-internal')
    if token is None:
        # prepare request input
        data = {'email': 'admin@admin.com', 'password': 'Password1'}

        # do request
        req = callClient(request)
        res = req.post('/token',
                       data=json.dumps(data),
                       content_type='application/json')
        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 200

        # save token into cache
        cache.set('token-internal', res_json['token'], timeout=60)

        # return because it useful for other test
        return res_json['token']
    else:
        return token
