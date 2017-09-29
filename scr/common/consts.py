# -*- coding: utf-8 -*-

class RespCode(object):
	# 基础code
	OKAY = 0
	FAILED = 1
	METHOD_GET_NOT_ALLOWED = 10
	UNKNOWN_ERROR = 999

	# 参数不包含data
	NO_INPUT_DATA = 100

	# 字段解析错误及解析错误
	WRONG_DATA_PARSE = 101
	WRONG_DATA_FORMAT = 102

	# 基础参数丢失
	NO_INPUT_MODULE = 110 		#没有该模块
	NO_INPUT_SERVICE = 111		#没有该接口
	NO_INPUT_PARAMETERS = 112	#没有输入字段
	NO_INPUT_SESSION = 113		#没有输入session
	ILLEGAL_PARAMS = 114 		#不合法字段

	# 检查合法的session
	INVALID_PARAM_MODULE = 120
	INVALID_PARAM_SERVICE = 121
	INVALID_PARAM_SESSION = 122
	MISSING_SPECIFIC_PARAMETER = 123
	WRONG_PARAMTER_FORMAT = 124

	VERSION_TOO_LARGE = 130

	ACCOUNT_PASSWORD_ERROR = 200	#用户名或密码错误
	USER_NOT_EXIST = 201			#用户不存在
	USER_HAS_EXIST = 202			#用户名已存在
	NOT_SESSION = 203				#SESSION验证失败
	WRONG_PASSWORD = 204 			#密码错误
	UPDATE_PROFILE_FAIL =205		#更新个人信息错误
	GET_PROFILE_FAIL = 206			#获取个人信息失败
	UPDATE_MOBILE_ACCOUNT_FAIL = 207#更新失败
	BIND_WECHAT_UNION_FAIL	=208	#绑定union码失败
	PHONE_HAS_EXIST = 209			#手机号码已存在

	NOT_AUTHORIZED_ACCOUNT = 220	# 未被授权的用户

	SET_CURRENT_PET_ERROR = 210		# 设置宠物错误
	NOT_EXISTED_DEFAULT_PET = 211	# 不存在的默认PET
	GENERATE_PET_ERROR = 212		# 生成宠物错误
	VIN_HAS_EXCITED = 213			# vin码已经存在
	NO_LOGIN_CLINE = 214			# 没有注册过的用户

	NO_SESSION = 215				# 其他地方被登录

	#购买道具
	NO_ITEM = 231				#没有该道具
	LACK_OF_MONEY = 232			#金币不足
	PURCHASE_FAILURE = 233		#购买失败
	USED_FAIL = 234				#使用失败

	#宠物技能
	NOT_EXISTED_SKILL = 240 	#没有该技能
	USED_SKILL_FAIL = 241		#释放失败
	GET_COST_FAIL = 242			#获取升级消耗失败
	UPGRADE_SKILL_FAIL = 243	#升级失败
	HIGHEST_RANK =244			#已达到最高级

	#好友
	UNFRIEND_FAIL = 250			#移除失败
	ADD_FRIEND_FAIL = 251		#添加失败
	ALREADY_ADDED = 252			#已添加
	NO_FRIENDS	=253			#未添加该好友
	ERROR_ID =254				#错误ID
	GET_FRIENDS_FAIL= 255		#获取好友失败

	#验证码
	REQUIST_TOO_FREUENTLY = 301		#请求太频繁
	REQUIST_FAIL = 302				#获取验证失败
	AUTH_FAILED = 303				#验证失败
	SEND_NOFIFICATION_FAIL = 304	#通知失败

	#微信
	ADD_VALIDATION_INFO_FAIL = 311	#添加验证信息失败
	NO_VALIDATION	= 312			#没有验证信息
	NO_CUUPON = 314					#没有抽中卡券
	COUPON_UNUSABLE = 315			#卡券不可用
	
	BUILD_PARKOUR_DATA_FAILED = 400
	ADD_COIN_FAILED = 401
	SET_MAX_SCORE_FAILED = 402
	TARGET_PET_NOT_FOUND = 403

	ABNORMAL_ERR = 506  #处理出现异常

	#用户Code
	USER_CREATE_FAILED = 600
	USER_UPDATE_FAILED = 601
	USER_DELETE_FAILED = 602
	USER_SET_ACTIVE_FAILED = 603

	UPLOAD_IMAGE_FAILED = 700

	#商店
	SHOP_HAS_EXISRT = 850		#商店已经存在

class RespBody(object):
	OKAY = '{"code":0,"response":%s}'
	ERROR = '{"code":%d}'

class MaintenanceProcessCode(object):
	NEW_ORDER = 1
	DESIGNATED_ENGINEER = 2
	ARRIVE = 3
	IN_MAINTENANCE = 4
	DONE = 5

class MaintenanceFinalCode(object):
	UNFINISHED = 1
	FINISHED = 2


class UserType(object):
	NORMAL = 10
	MOBILE = 11


class LoginType(object):
	APP = 1
	WECHAT = 2
	MALL = 3
	BBS = 4
	SPORT = 5

class WorkStatus(object):
	FREE = 0
	BUSY = 1


class OrderType(object):
	FAULT = 1	#故障
	QUICK_SERVICE = 2	#快修