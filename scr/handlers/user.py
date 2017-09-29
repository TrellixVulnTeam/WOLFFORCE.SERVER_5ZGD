# -*- coding: utf-8 -*-

import random
import asyncio
import time
from tornado import gen  #异步

from model.user import UserService
from model.auth import AuthService
from model.ranking import RankingService
from common.consts import RespCode

class UserHandler(object):

	def __init__(self):
		self.__srv_user = UserService()
		self.__srv_auth = AuthService()
		self.__srv_rank = RankingService()

	# 发送验证码
	@asyncio.coroutine
	def send_verify_code(self , params):
		phone_num = params['mobile']

		request = yield from self.__srv_auth.sendcode(phone_num)
		if not request:
			return RespCode.REQUIST_FAIL
		return RespCode.OKAY

	# 注册
	@asyncio.coroutine
	def register_user(self , params):
		mobile = params['mobile']
		code = params['code']
		username = params['username']
		password = params['password']

		has_user =  yield from self.__srv_user.has_user(username)
		has_mobile_user = yield from self.__srv_user.has_mobile_user(mobile)
		if has_user:
			return RespCode.USER_HAS_EXIST
		elif has_mobile_user:
			return RespCode.PHONE_HAS_EXIST
		else:
			# request =  yield from self.__srv_auth.verifycode(mobile, code)
			# if request:
			add_user = yield from self.__srv_user.add_user(mobile, username, password)
			# else:
			# 	return RespCode.AUTH_FAILED
		if add_user :		#如果添加用户成功
			user_id = yield from self.__srv_user.get_username_by_id(username)

			# 检查该用户是否玩过游戏
			history_kill_number = yield from self.__srv_rank.check_ranking_user(user_id)
			if str(type(history_kill_number)).find('bool') == 8:
				#首次注册，先在排行榜列表里面添加占位数据
				add_ranking_user = yield from self.__srv_rank.add_ranking_user(user_id, 0, 0, 0)

				if add_ranking_user:
					return RespCode.OKAY
				else:
					return RespCode.FAILED
			return RespCode.OKAY
		else:
			return RespCode.FAILED


	#以用手机号码和验证码登录
	@asyncio.coroutine
	def login_with_verify_code(self , params):
		mobile = params['mobile']
		code = params['code']

		request =  yield from self.__srv_auth.verifycode(mobile, code)
		if not request :
			return RespCode.AUTH_FAILED  #验证码验证失败
		has_mobile_user = yield from self.__srv_user.has_mobile_user(mobile)
		if not has_mobile_user:
			return RespCode.USER_NOT_EXIST
		user_session =  yield from self.__srv_user.update_session(mobile)
		if not user_session:
			return RespCode.FAILED       #修改session失败
		res = {
			'session': user_session
		}
		return res

	# 使用用户名和密码登录
	@asyncio.coroutine
	def login_with_username_and_password(self , params):
		username = params['username']
		password = params['password']

		# 检查用户名是否存在
		has_user =  yield from self.__srv_user.has_user(username)
		has_mobile_user = yield from self.__srv_user.has_mobile_user(username)
		if not has_user and not has_mobile_user:
			return RespCode.USER_NOT_EXIST
		check_password = yield from self.__srv_user.check_password(username, password)
		if not check_password:
			return RespCode.WRONG_PASSWORD
		user_session =  yield from self.__srv_user.update_session(check_password)
		if not user_session:
			return RespCode.FAILED
		res = {
			'session': user_session
		}
		return res

	#获取用户基本资料
	@asyncio.coroutine
	def get_user_info(self, params):
		user_id = params['user_id']
		user_info = yield from self.__srv_user.get_user_info(user_id)

		print(user_info)
		return user_info
	
	#修改用户的基本信息
	@asyncio.coroutine
	def update_user_info(self , params):
		user_id = params['user_id']
		username = params['username']
		password = params['password']
		store = params['store']
		icon = params['icon']

		updata_user_info = yield from self.__srv_user.update_user_info(user_id, username, password, store, icon)
		if updata_user_info :
			return RespCode.OKAY
		else:
			return RespCode.FAILED
