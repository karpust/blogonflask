# вынесли конфиг отдельно
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://n:5236@localhost:5432/blog_db'
    # URI for connection:
    # dialect+driver://username:password@host:port/database_name
    # https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
    SECRET_KEY = '67dc3db4f4a542a544b08dce5100104fa59a670e7c8bd8291155e865eaabb61d'
    # to generate SECRET_KEY: python -c 'import secrets; print(secrets.token_hex())'

