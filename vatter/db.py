from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import settings


engine = create_engine(settings.DB_PATH)
Session = sessionmaker(bind=engine)
