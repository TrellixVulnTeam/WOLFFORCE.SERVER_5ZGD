
# 注册
# http://192.168.1.58:10040/user?data={"module":"user","service":"register_user","session":"","parameters":{"mobile":"18829207378","code":"1234","username":"你好","password":"8935847598"}}

# 登录
# http://192.168.1.58:10040/user?data={"module":"user","service":"login_with_verify_code","session":"","parameters":{"mobile":"18829207378","code":"1234"}}

# http://192.168.1.58:10040/user?data={"module":"user","service":"login_with_username_and_password","session":"","parameters":{"username":"18829207378","password":"1234"}}
# 

# 获取用户基本信息

# http://192.168.1.58:10040/user?data={"module":"user","service":"get_user_info","session":"a2f1ffc305c539697e78411aed9661e2","parameters":{}}

# 修改个人信息
# http://192.168.1.58:10040/user?data={"module":"user","service":"update_user_info","session":"a2f1ffc305c539697e78411aed9661e2","parameters":{"username":"杨先辉","password":"123","store":"第一","icon":"  "}}


# 更新排行榜
# http://192.168.1.58:10040/user?data={"module":"ranking","service":"upload_performance","session":"a2f1ffc305c539697e78411aed9661e2","parameters":{"score":"136521","kill_number":"123","continue_time":"13:20:2"}}

# 获取排行榜
# http://192.168.1.58:10040/user?data={"module":"ranking","service":"get_ranking","session":"7c96d4b41af8d776a0e2fc98d2b8f92e","parameters":{}}











