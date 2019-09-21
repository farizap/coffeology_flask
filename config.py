class Config():
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:alta321@localhost:3306/finalProject'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Altabatch3@coffeologydb.cve4hruuas3j.ap-southeast-1.rds.amazonaws.com:3306/coffeology'
    
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://adesupraptolaia:alta123@localhost:3306/finalProject'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:alta321@localhost:3306/finalProject_test'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://adesupraptolaia:alta123@localhost:3306/finalProject_test'