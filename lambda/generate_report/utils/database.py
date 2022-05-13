import json
import os
from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.database_schema import Step
from utils.log import Log

Session = sessionmaker()


class Database(object):
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r', encoding='UTF-8') as file:
            self.config = json.load(file)
        engine = self.create_engine()
        Session.configure(bind=engine)
        self.session = Session()

    def create_engine(self):
        db_config = self.config['database']
        adapter = db_config['adapter']
        host = db_config['host']
        port = db_config['port']
        database = db_config['database']
        user = db_config['user']
        password = db_config['password']
        db_uri = f'{adapter}://{user}:%s@{host}:{port}/{database}' % quote(password)
        return create_engine(db_uri, echo=False)

    def insert_log(self, log: Log):
        new_log = Step(
            page=log.page,
            test=log.test,
            is_summary=log.is_summary,
            step=log.step,
            log_dt=log.log_dt,
            spent_time=log.spent_time
        )
        self.session.add(new_log)
        self.session.commit()
