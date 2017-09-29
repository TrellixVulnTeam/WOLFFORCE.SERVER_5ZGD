# -*- coding: utf-8 -*-

import asyncio

from common.database import MySQL

class BaseService(object):
	def __init__(self):
		self.__tran = None
		self.__conn = None

	# 初始化数据库连接，由于被连接池接管，不用担心性能问题
	@asyncio.coroutine
	def _init_db(self, db_id = 1):		# 实例化数据库
		self.__conn = yield from MySQL.get_connection(db_id)
		self.__tran = yield from MySQL.get_transaction(self.__conn)

	# 释放数据库连接，每次完成数据库连接的使用必须释放，否则产生内存泄漏！
	@asyncio.coroutine
	def _release_db(self):
		if self.__conn != None:
			yield from self.__conn.close()   #关闭链接
			self.__conn = None

		if self.__tran != None:
			if self.__tran.is_active:
				yield from self.__tran.commit()			#提交数据
			self.__tran = None

	@property
	def _conn(self):		#获取链接
		return self.__conn

	@property
	def _tran(self):		#获取事物
		return self.__tran
