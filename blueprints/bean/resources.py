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
        # bean = Beans.query.get(id)
        bean="as"
        if bean is not None:
            # beanData = marshal(bean, Beans.responseFields)
            beanData = {
                'id': 1,
                'originID': 1,
                'name': "bean1",
                'photo':
                    "http://3.bp.blogspot.com/-NlbLDQ72yfg/VgLQFnMkCSI/AAAAAAAADaY/eiX1XdNv0uI/s1600/kopiaceh.jpg",
                'fragrance': 0.4,
                'flavor': 0.4,
                'aftertaste': 0.5,
                'acidity': 0.5,
                'body': 0.5,
                'balance': 0.5,
                'uniformity': 0.3,
                'cleanCups': 0.5,
                'sweetness': 0.3,
                'overall': 0.4,
                'description':
                    "Coffee trees are planted in Jernih Jaya Village locate Arabica Simalungun Location: North Sumatera cupping: September 2017 by Gayo Cuppers Team in Gunung Tujuh, Kerinci District, Jambi Province. Coffee plantation are grown in the altitute od 1,200 - 1,400 meter above sea level in the Mount Kerinci areas. Beside of coffee, the location is well known for agro tourism.",
                'cupping': "cupping",
                'advantage': "advantage1,gggadvantage1",
                'disadvantage': "disadvantage1,disadvantage2,disadvantage3",
                'location': "location"
            },
            beanAdvantages = beanData['advantage']
            beanData['advantage'] = beanAdvantages.split(',')
            beanDisadvantages = beanData['disadvantage']
            beanData['advantdisadvantageage'] = beanDisadvantages.split(',')
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
            beanByOriginID = beans.filter_by(originID=number)
            beanTemporaryList = []
            for bean in beanByOriginID:
                beanTemporaryList.append(marshal(bean, Beans.responseFieldsGetAll))
            listBean[number] =  beanTemporaryList

        return {'code': 200, 'message': 'oke', 'data': listBean}, 200


api.add_resource(BeanListResource, '')
api.add_resource(BeanResource, '/<id>')
