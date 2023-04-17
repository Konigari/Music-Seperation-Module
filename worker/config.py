import os

class Config(object):
        # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        # GET_HOSTS_FROM = os.environ.get('GET_HOSTS_FROM') or 'dns'

        REDIS_SERVICE_HOST = os.environ.get('REDIS_SERVICE_HOST') or 'localhost'
        REDIS_SERVICE_PORT = os.environ.get('REDIS_SERVICE_PORT') or 6379

        MINIO_SERVICE_HOST = os.environ.get('MINIO_SERVICE_HOST') or 'localhost'
        MINIO_SERVICE_PORT = os.environ.get('MINIO_SERVICE_PORT') or 9000
        MINIO_USER = "rootuser"
        MINIO_PASSWD = "rootpass123"