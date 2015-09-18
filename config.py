#encoding=utf-8
#保存各类设定
import os
import psycopg2
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <490472721@qq.com>'
    FLASKY_ADMIN = '490472721@qq.com'
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    SSL_DISABLE = False

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://b64539cf752daa:8c85a8b3@us-cdbr-iron-east-02.cleardb.net/heroku_1838b36d08e9b2b'

    @classmethod
    def init_app(cls,app):
        Config.init_app(app)


class DevelopmentConfig(Config):
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}
