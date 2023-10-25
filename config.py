class Config(object):
    DEBUG = True
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True
    PERMANENT_SESSION_LIFETIME = 1200
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/sipp_log'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "AFSBAKFBAKBFAK0987fsghajklksjhgeywuiueyuskxncbnxm"
    CSRF_ENABLED = True

class ProductionConfig(Config):
	DEBUG = False

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True