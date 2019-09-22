from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Beans
from sqlalchemy import desc
from blueprints import app, db, internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims
import re
import hashlib

bp_beans = Blueprint('beans', __name__)
api = Api(bp_beans)


class BeanResource(Resource):
    def __init__(self):
        pass

    def options(self, id=None):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self, id):
        bean = Beans.query.get(id)
        if bean is not None:
            beanData = marshal(bean, Beans.responseFields)
            return {
                'code': 200,
                'message': 'oke',
                'data': beanData
            }, 200
        return {'code': 404, 'message': 'Bean Not Found'}, 404

class BeanListResource(Resource):
    def __init__(self):
        pass

    def options(self):
        return {'code': 200, 'message': 'oke'}, 200

    def get(self):
        beans = Beans.query

        listBean = {}
        # show result with filter by origin ID
        for number in range(1,6):
            beanByOriginID = Beans.query.filter_by(originID=number)
            beanTemporaryList = []
            for bean in beanByOriginID.all():
                beanTemporaryList.append(marshal(bean, Beans.responseFieldsGetAll))
            listBean[number] =  beanTemporaryList

        return {'code': 200, 'message': 'oke', 'data': listBean}, 200


api.add_resource(BeanListResource, '')
api.add_resource(BeanResource, '/<id>')
