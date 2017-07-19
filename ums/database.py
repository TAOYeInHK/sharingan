# -*- coding:utf-8 -*-
from contextlib import contextmanager

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ums import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session = db.sessionmaker()
Session.configure(bind=db.engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

