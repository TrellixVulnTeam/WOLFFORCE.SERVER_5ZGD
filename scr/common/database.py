# -*- coding: utf-8 -*-

import asyncio
import asyncio_redis
import aiomysql.sa
from sqlalchemy import *
from sqlalchemy.orm import *

from common.dao import TableSet
from common.utils import Debug


class MySQL(object):
	__metadata = None
	__engine = {}
	__tbl_journal_list = None

	#创建数据库 engine
	@staticmethod
	@asyncio.coroutine
	def initialize(address, port, user, passwd, db_name, db_id, db_charset, maxpoolsize):
		MySQL.__metadata = MetaData()
		TableSet.build(MySQL.__metadata)
		MySQL.__engine[db_id] = yield from aiomysql.sa.create_engine(
			host = address,
			port = port,
			user = user,
			password = passwd,
			db = db_name,
			charset = db_charset,
			maxsize = maxpoolsize
		)

	#获取链接
	@staticmethod
	@asyncio.coroutine
	def get_connection(db_id):
		conn = yield from MySQL.__engine[db_id].acquire()
		return conn

		# with (yield from MySQL.__engine) as conn:
		# 	return conn

	# @staticmethod
	# @asyncio.coroutine

	#获取事务
	@staticmethod
	@asyncio.coroutine
	def get_transaction(conn):
		tran = yield from conn.begin()
		return tran
