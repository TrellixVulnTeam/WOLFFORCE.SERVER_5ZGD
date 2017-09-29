# -*- coding: utf-8 -*-
import random
import asyncio
import time

from model.ranking import RankingService
from common.consts import RespCode


class RankingHandler(object):

	def __init__(self):
		self.__srv_rank = RankingService()

# 	更新排行榜
	@asyncio.coroutine
	def upload_performance(self , params):
		user_id = params['user_id']
		last_score = params['score']							#上次分数
		last_kill_number = params['kill_number'] 				#上次击杀人数
		last_continue_time = params['continue_time']		    #上次持续时间

		# 检查该用户是否玩过游戏
		history_kill_number = yield from self.__srv_rank.check_ranking_user(user_id)

		if str(type(history_kill_number)).find('bool') == 8:
			# 首次创建成绩
			add_ranking_user = yield from self.__srv_rank.add_ranking_user(user_id, last_score, last_kill_number, last_continue_time)
			if add_ranking_user :
				return RespCode.OKAY
			else:
				return RespCode.FAILED
		else:
			# 更新最高
			upload_performance = yield from self.__srv_rank.upload_ranking(history_kill_number, user_id, last_score, last_kill_number, last_continue_time)
			if not upload_performance:
				return RespCode.FAILED
			else:
				return RespCode.OKAY

	@asyncio.coroutine
	def get_ranking(self, params):
		all_ranking = yield from self.__srv_rank.get_ranking_me()
		if all_ranking:
			return all_ranking
		else:
			return RespCode.FAILED
