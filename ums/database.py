# -*- coding:utf-8 -*-
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

from ums import app
db = SQLAlchemy(app)
Session = db.sessionmaker()


@contextmanager
def session_scope(**kwargs):
    """Provide a transactional scope around a series of operations."""
    external_session = kwargs.pop('session', None)
    session = external_session or Session(**kwargs)
    try:
        yield session
        external_session or session.commit()
    except:
        external_session or session.rollback()
        raise
    finally:
        external_session or session.close()

