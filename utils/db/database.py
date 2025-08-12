import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ParsedData(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    for_whom = Column(String)
    problem_solved = Column(String)

class Database:
    def __init__(self, db_path: str):
        self.logger = logging.getLogger(__name__)
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.logger.info("Database initialized")

    def add_project(self, url: str, name: str, for_whom: str, problem_solved: str):
        with self.Session() as session:
            data = ParsedData(url=url, name=name, for_whom=for_whom, problem_solved=problem_solved)
            session.add(data)
            session.commit()
            self.logger.info("Data successfully added to database")