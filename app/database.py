from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"  #"postgresql+psycopg://postgres:123456@localhost:5432/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Session_local = sessionmaker(bind=engine,autoflush=False,autocommit = False)

Base = declarative_base()


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect(
#             host = 'localhost',
#             dbname = 'fastapi',
#             user = 'postgres',
#             password = '123456',
#             row_factory=dict_row

#         )
#         cursor = conn.cursor()
#         print("Database Connected successfully!")

#         break

#     except Exception as error:
#         print("Error connecting to database:", error)
#         time.sleep(2)
