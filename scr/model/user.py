# -*- coding: utf-8 -*-

import random
import json
import asyncio
import time
import datetime
# from datetime import datetime
from sqlalchemy import and_, or_

from common.dao import TableSet
from common.utils import md5hash

from model.base import BaseService

class UserService(BaseService):

	# 用户名--检查用户是否存在
	@asyncio.coroutine
	def has_user(self, username):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.user.select(
				TableSet.user.c.account == username
			)
		)
		yield from self._release_db()
		return result.rowcount > 0

	# 检查用户--通过手机号码
	@asyncio.coroutine
	def has_mobile_user(self, phone_number):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.user.select(
				TableSet.user.c.phone_number == phone_number
			)
		)
		yield from self._release_db()
		return result.rowcount > 0

	# 通过手机号码获取用户名
	@asyncio.coroutine
	def get_username_by_mobile(self, phone_number):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.user.select(
				TableSet.user.c.phone_number == phone_number
			).limit(1)
		)
		yield from self._release_db()
		if result.rowcount < 0:
			return False
		row = yield from result.fetchone()
		user_name = row.account
		return user_name

	# 检查session
	@asyncio.coroutine
	def get_username_by_session(self, session):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.user.select(
				TableSet.user.c.session == session
			).limit(1)
		)
		yield from self._release_db()
		user_id = None
		phone_number = None
		if result.rowcount > 0:
			# row = yield from result.fetchone()
			
			for row in result:
				user_id = row.id
				phone_number = row.phone_number

		return phone_number, user_id

	# 通过用户名获取用户ID
	@asyncio.coroutine
	def get_username_by_id(self, account):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.user.select(
				TableSet.user.c.account == account
			).limit(1)
		)
		yield from self._release_db()
		user_id = None
		if result.rowcount > 0:
			# row = yield from result.fetchone()
			for row in result:
				user_id = row.id

		return  user_id

	# 设置session
	@asyncio.coroutine
	def update_session(self, mobile):
		new_session = md5hash(mobile + str( random.randint(1, 100000000)) + str(time.time() ) )
		print("new_session : " + new_session)
		yield from self._init_db()
		try :
			result = yield from self._conn.execute(
				TableSet.user.update(
					TableSet.user.c.phone_number == mobile
				).values(
					session = new_session
				)
			)
			yield from self._tran.commit()
			yield from self._release_db()
			return new_session
		except:
			yield from self._tran.rollback()
			yield from self._release_db()
			return False

	# 通过session获取用户信息
	@asyncio.coroutine
	def get_user_info(self, user_id):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.user.join(
				TableSet.ranking, 
				TableSet.ranking.c.user_id == TableSet.user.c.id
			).select(
				TableSet.user.c.id == user_id
			)
		)
		yield from self._release_db()
		user = {}
		for row in result:
			user['name'] = row.account
			user['store'] = row.store
			user['icon'] = row.icon
			user['history_highest_score'] = row.history_highest_score
			user['history_kill_number'] = row.history_kill_number
			user['history_continue_time'] = row.history_continue_time
			user['last_score'] = row.last_score
			user['last_kill_number'] = row.last_kill_number
			user['last_continue_time'] = row.last_continue_time
			user['updata_time'] = (str)(row.updata_time)

		return user
	
	# 通过session检查用户是否在线
	@asyncio.coroutine
	def get_is_online_by_session(self, session):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.user.select(
				TableSet.user.c.session == session
			).limit(1)
		)
		yield from self._release_db()
		online = None
		if result.rowcount > 0:
			row = yield from result.fetchone()
			return  row.online

	# 检查密码
	@asyncio.coroutine
	def check_password(self, username, password):
	
		yield from self._init_db()
		result  = yield from self._conn.execute(
			TableSet.user.select(
				and_(
					TableSet.user.c.password == md5hash(password),
					or_(
						TableSet.user.c.account == username,
						TableSet.user.c.phone_number == username
					)
				)
				
			).limit(1)
		)
		yield from self._release_db()
		if result.rowcount > 0:
			row = yield from result.fetchone()
			return row.phone_number
		else:
			return False

	# 手机号码--添加用户
	@asyncio.coroutine
	def add_user(self, mobile, username, password):

		yield from self._init_db()
		time = datetime.datetime.now()
		try:
			result = yield from self._conn.execute(
				TableSet.user.insert().values(
					phone_number = mobile,
					account = username,
					password = md5hash(password),
					create_time = time
				)
			)
			yield from self._tran.commit()
			yield from self._release_db()
			return True
		except:
			yield from self._tran.rollback()
			yield from self._release_db()
			return False

	# 修改个人信息
	@asyncio.coroutine
	def update_user_info(self, user_id, account, password, store, icon):
		print(user_id)

		yield from self._init_db()
		try:
			result = yield from self._conn.execute(
				TableSet.user.update(
					TableSet.user.c.id == user_id
				).values(
					account = account,
					store = store,
					icon = icon,
					password = md5hash(password)
				)
			)
			yield from self._tran.commit()
			yield from self._release_db()
			return True
		except:
			yield from self._tran.rollback()
			yield from self._release_db()
			return False