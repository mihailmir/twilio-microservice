import os


class Envs:
    ENV = os.getenv('ENV', "DEV")
    APP_HOST = os.getenv('APP_HOST')
    APP_PORT = int(os.getenv('APP_PORT'))

    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_FROM = os.getenv('EMAIL_FROM')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_NAME = os.getenv('EMAIL_NAME')

    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')

    SUPPORT_EMAIL_1 = os.getenv('SUPPORT_EMAIL_1')
    SUPPORT_EMAIL_2 = os.getenv('SUPPORT_EMAIL_2')
    SUPPORT_EMAIL_3 = os.getenv('SUPPORT_EMAIL_3')
    SUPPORT_EMAIL_4 = os.getenv('SUPPORT_EMAIL_4')

    CURRENT_DOMAIN = os.getenv('CURRENT_DOMAIN')
