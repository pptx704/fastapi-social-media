import os

SECRET_KEY = os.environ.get("JWT_SECRET", "fb89174cce0281e275407cb7d948e858")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", 240))

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', "postgresql://postgres:admin@localhost:5432/flask-social-media")

HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY", "44b07e77ce15bbec6a51dbe7283188ca")