from __future__ import absolute_import, unicode_literals
import pymysql

pymysql.install_as_MySQLdb()


# This will make sure the app is always imported when
# Django starts so Celery works properly.
from .celery import app as celery_app

__all__ = ['celery_app']
