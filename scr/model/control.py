# -*- coding: utf-8 -*-

import json
import asyncio

from common.dao import TableSet

from model.base import BaseService

class ControlService(BaseService):

	@asyncio.coroutine
	def set_game_state(self , switch):
		yield from self._init_db()

		try:
			yield from self._conn.execute(

				TableSet.control.update(
					TableSet.control.c.id == 1
				).values(
					off_or_on = switch
				)
			)
			yield from self._tran.commit()
			yield from self._release_db()
			return True
		except:
			yield from self._tran.rollback()
			yield from self._release_db()
			return False

	@asyncio.coroutine
	def get_game_state(self):

		yield from self._init_db()
		result = yield from self._conn.execute(
			TableSet.control.select(
				TableSet.control.c.id == 1
			)
		)

		yield from self._release_db()

		if result.rowcount > 0:
			row = yield from result.fetchone()
			print('dadfasfafs : ' + str(result.rowcount))
			return row.off_or_on > 0
		else:
			return False
		