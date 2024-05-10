from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    print("Path of the file is not found")
    config = Config("")  # Define config with an empty Config object if file not found

SECRET_KEY = config("DATABASE_URL", cast=Secret)


""" 
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from dotenv import load_dotenv
# from typing import Optional
# from sqlalchemy import URL
# import os

# load_dotenv()

# SQLALCHEMY_DATABASE_URL: Optional[str | URL] = os.getenv("DATABASE_URL")

# if not SQLALCHEMY_DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set or invalid")

# # connect_args = ("check_same_thread", False)
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # db = SessionLocal()
# # with SessionLocal() as s:


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# Base = declarative_base()
 """
