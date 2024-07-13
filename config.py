import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

# Load environment variables from the .env file
load_dotenv()

# Parse the database URL and adjust the scheme if necessary
database_url = os.getenv('DATABASE_URL')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

class Config:
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
