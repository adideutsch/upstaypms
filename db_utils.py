import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from config import DB_DIALECT, DB_DRIVER, DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT


def get_db_engine():
    return db.create_engine(f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}')


def get_db_session():
    return sessionmaker(bind=get_db_engine())()
