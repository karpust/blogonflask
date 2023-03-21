class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/postgre_db'
    # URI for connection from
    # https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
    # "postgresql://postgres:postgres@localhost:5432/cars_api"
    SECRET_KEY = '67dc3db4f4a542a544b08dce5100104fa59a670e7c8bd8291155e865eaabb61d'
    # to generate SECRET_KEY: python -c 'import secrets; print(secrets.token_hex())'

