import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

import config


SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://{}:{}@{}/data'.format(config.username, config.password,
                                                                             config.db_address)

engine = sql.create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative.declarative_base()
