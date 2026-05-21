# fake_image_detector/__init__.py
from __future__ import absolute_import, unicode_literals

# import pymysql
#
# pymysql.install_as_MySQLdb()

# 允许在未安装 Celery 的环境中运行管理命令，如 makemigrations。
try:
    from .celery import app as celery_app
except ModuleNotFoundError:
    celery_app = None

__all__ = ('celery_app',)
