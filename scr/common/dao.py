# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import SmallInteger, Integer
from sqlalchemy import Float
from sqlalchemy import String, UnicodeText
from sqlalchemy import DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

class TableSet(object):
	journal = None
	user = None

	@staticmethod
	def build(metadata):
		TableSet.user = Table(
			'user_tbl', metadata,
			Column('id', Integer, primary_key = True, autoincrement = True),
			Column('account', String, primary_key = True, nullable = False),
			Column('phone_number', String, primary_key = True, nullable = False),
			Column('store',String, primary_key = True, nullable = True),
			Column('password', String, primary_key = True, nullable = False),
			Column('icon', String, nullable = True),
			Column('level', Integer, primary_key = True, nullable = True),
			Column('score', Integer,primary_key = True, nullable = True),
			Column('create_time', DateTime, primary_key = True, nullable = False),
			Column('last_login_time', DateTime),
			Column('session', String, primary_key = True, nullable = True),
			Column('online', Integer, primary_key = True, nullable = False)
		)

		TableSet.ranking = Table(
			'ranking_list_tbl', metadata,
			Column('id', Integer, primary_key = True, autoincrement = True),
			Column('user_id', Integer, primary_key = True,  nullable = True),
			Column('history_highest_score',  Integer, primary_key = True,  nullable = True),
			Column('history_kill_number', Integer, primary_key = True, nullable = True),
			Column('history_continue_time', String, primary_key = True, nullable = True),
			Column('last_score', Integer, nullable = True),
			Column('last_kill_number', Integer, nullable = True),
			Column('last_continue_time', String, nullable = True),
			Column('death_number', Integer, nullable = True),
			Column('updata_time', DateTime, nullable = True)
		)

		TableSet.control = Table(
			'switch', metadata,
			Column('id', Integer, primary_key = True, nullable = False),
			Column('off_or_on', Integer, primary_key = True, nullable = False)
		)