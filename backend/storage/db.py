import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.logger import logger

db_str = os.environ.get("DB")
if db_str is None:
    logger.error("DB env is None")
    exit(1)
engine = create_engine(db_str, echo=False)

Session = sessionmaker(autoflush=False, bind=engine)
