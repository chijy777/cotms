import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    'mysql://root:youtiandai0)@123.56.201.94/cotms',
    pool_recycle=60,
    connect_args={"charset": "utf8"},
    echo=True
)

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))

