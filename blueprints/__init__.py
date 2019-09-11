from flask import Flask, request
import json, os
# Import yang dibutuhkan untuk database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
from flask_cors import CORS
import config

app = Flask(__name__)
CORS(app)
###################################
# JWT
###################################

# Bisa bebas
app.config['JWT_SECRET_KEY'] = 'zENpazwq97E5BqkFUcAdc9ssMqnRMuufe7aQDHYc'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']:  # If berjalan jika statement True, jadi 'not False' = True
            return {'status': 'FORBIDDEN', 'message': 'Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# Buat Decorator untuk non-internal

def non_internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status']:  # If berjalan jika statement True, jadi 'not False' = True
            return {'status': 'FORBIDDEN', 'message': 'Non-Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

except Exception as e:
    raise e



# Setting Database
app.config['APP_DEBUG'] = True
# localhost aka 127.0.0.1

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Altabatch3@ecommerce.ctfwww9400s4.ap-southeast-1.rds.amazonaws.com:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# log error (middlewares)
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()

    app.logger.warning("REQUEST_LOG\t%s",
                       json.dumps({
                           'method': request.method,
                           'code': response.status,
                           'uri': request.full_path,
                           'request': requestData,
                           'response': json.loads(response.data.decode('utf-8'))
                       }))
    return response


from blueprints.user.resources import bp_users
from blueprints.method.resources import bp_methods
from blueprints.recipe.resources import bp_recipes
from blueprints.step.resources import bp_steps

app.register_blueprint(bp_users, url_prefix='/users')
app.register_blueprint(bp_methods, url_prefix='/methods')
app.register_blueprint(bp_recipes, url_prefix='/recipes')
app.register_blueprint(bp_steps, url_prefix='/steps')

db.create_all()
