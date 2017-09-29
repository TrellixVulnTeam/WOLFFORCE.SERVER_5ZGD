# -*- coding: utf-8 -*-
import random
import json
import asyncio
import time
import datetime
from sqlalchemy import and_

from common.dao import TableSet
from common.utils import md5hash

from model.base import BaseService

class RankingService(BaseService):

	# 检查用户是不是在排行榜内部
	@asyncio.coroutine
	def check_ranking_user(self , user_id):
		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.ranking.select(
				TableSet.ranking.c.user_id == user_id
			).limit(1)
		)
		yield from self._release_db()
		history_kill_number = 0
		if result.rowcount>0:
			for row in result:
				history_kill_number = row.history_kill_number
			return history_kill_number
		else:
			return False

	# 更改排行榜分数
	@asyncio.coroutine
	def upload_ranking(self , history_kill_number, user_id, last_score, last_kill_number, last_continue_time):
		updata_time = datetime.datetime.now()

		# 判端是否需要更新历史最高
		if history_kill_number < int(last_kill_number):
			yield from self._init_db()
			try :
				result = yield from self._conn.execute(
					TableSet.ranking.update(
						TableSet.ranking.c.user_id == user_id
					).values(
						history_highest_score = int(last_score),
						history_kill_number = int(last_kill_number),
						history_continue_time = int(last_continue_time),
						last_score = last_score,
						last_kill_number = int(last_kill_number),
						last_continue_time = int(last_continue_time),
						updata_time = updata_time
					)
				)
				yield from self._tran.commit()
				yield from self._release_db()
				return True
			except:
				yield from self._tran.rollback()
				yield from self._release_db()
				return False
		else:
			yield from self._init_db()
			try :
				result = yield from self._conn.execute(
					TableSet.ranking.update(
						TableSet.ranking.c.user_id == user_id
					).values(
						last_score = int(last_score),
						updata_time = updata_time,
						last_continue_time = last_continue_time,
						last_kill_number = int(last_kill_number)
					)
				)
				yield from self._tran.commit()
				yield from self._release_db()
				return True
			except:
				yield from self._tran.rollback()
				yield from self._release_db()
				return False

	#新添加排行榜用户
	@asyncio.coroutine
	def add_ranking_user(self, user_id, last_score, last_kill_number, last_continue_time):
		updata_time = datetime.datetime.now()
		yield from self._init_db()
		try:
			yield from self._conn.execute(
				TableSet.ranking.insert().values(
					user_id = user_id,
					history_highest_score = last_score,
					history_kill_number = last_kill_number,
					history_continue_time = last_continue_time,
					last_score = last_score,
					last_kill_number = last_kill_number,
					last_continue_time = last_continue_time,
					updata_time = updata_time
				)
			)
			yield from self._tran.commit()
			yield from self._release_db()
			return True
		except:
			yield from self._tran.rollback()
			yield from self._release_db()
			return False

	# 获取前五十的排行
	@asyncio.coroutine
	def get_ranking_me(self):
		print(123)
		yield from self._init_db()
		result = yield from self._conn.execute(
			"select a.history_kill_number,a.history_highest_score,a.history_continue_time,b.account from ranking_list_tbl as a join user_tbl as b where a.user_id = b.id order by  a.history_kill_number desc,a.history_highest_score desc,a.history_continue_time desc limit 50"
		)
		yield from self._release_db()
		all_ranking = []
		for row in result:
			print('result name : ' + row.account)
			user = {}
			user['history_kill_number'] = row.history_kill_number
			user['history_highest_score'] = row.history_highest_score
			user['history_continue_time']= row.history_continue_time
			user['name'] = row.account
			all_ranking.append(user)
		print(all_ranking)
		return all_ranking
	

			
				
			
	