from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://root:1234@localhost/coderunner", echo=True)

Session = sessionmaker(autoflush=False, bind=engine)
