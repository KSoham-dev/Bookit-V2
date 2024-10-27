from datetime import timedelta
SECRET_KEY = "9J3a8cwcSzuZU7wErE6aqttewo2nDXSR4GeK5GPDlHY" ## Don't ever keep your secrets exposed in production 
DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
JWT_SECRET_KEY = "bc1712dfed677aa98ed886e0" ## Don't ever keep your secrets exposed in production 
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
CACHE_TYPE = "RedisCache"
CACHE_DEFAULT_TIMEOUT = 1800
CACHE_KEY_PREFIX = "bookitv2_cache"
CACHE_REDIS_URL = "redis://localhost:6379/1"
CELERY_BROKER_URL = "redis://localhost:6379/2"
CELERY_RESULT_BACKEND = "redis://localhost:6379/3"
CELERY_TIMEZONE = "Asia/Kolkata"
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USERNAME = "demobookitv2@gmail.com"
MAIL_PASSWORD = "iwhw clka octv fvex"
MAIL_USE_TLS = True
MAIL_USE_SSL = False
