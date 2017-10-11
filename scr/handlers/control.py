# -*- coding: utf-8 -*-

import asyncio
import time

from model.control import ControlService
from common.consts import RespCode


class ControlHandler(object):

	def __init__(self):
		self.__srv_control = ControlService()

	#设置游戏状态
	@asyncio.coroutine
	def change_game_state(self, params):

		off = int(params['off'])

		result = yield from self.__srv_control.set_game_state(off)

		if result:
			return RespCode.OKAY
		else:
			return RespCode.FAILED

	#获取游戏状态
	@asyncio.coroutine
	def get_game_state(self, params):
		result = yield from self.__srv_control.get_game_state()

		return result
