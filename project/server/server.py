from flask import Flask, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from gevent import pywsgi
import json, sys, configparser


config = configparser.ConfigParser()
config.read(sys.argv[1], encoding="utf-8")

# 框架初始化
app = Flask(__name__)
# 浏览器安全策略
CORS(app, supports_credentials=True)
# 数据库初始化
mysql = SQLAlchemy()
# 连接方式 {数据库类型}+{驱动类型}://{用户名}:{密码}@{数据库地址}:{数据库端口，默认3306}/{使用的数据库}
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s:%d/%s' % (
    config.get('mysql', 'user'),
    config.get('mysql', 'password'),
    config.get('mysql', 'host'),
    config.getint('mysql', 'port'),
    config.get('mysql', 'database'),
)
app.config['SQLALCHEMY_ECHO'] = config.getboolean('mysql', 'debug')
mysql.init_app(app)


# 读操作
def query(sql, param=None):
    results = mysql.session.execute(sql, param)
    data = [dict(zip(result.keys(), result)) for result in results]
    return data


# 写操作
def execute(sql, param):
    result = mysql.session.execute(sql, param)
    mysql.session.commit()
    return result


@app.before_request
def before_request():
    if request.path == '/login':
        return None

    if request.cookies.get("id") is None:
        return response(9999, "登录信息失效，请重新登陆")
    return None


@app.after_request
def after_request(resp):
    resp.headers["Content-Type"] = "application/json"
    return resp


@app.route('/')
def hello_world():
    return 'Hello World!'


# 默认是get请求，若需要使用post方法，需要显式的配置post
@app.route('/index')
def hello_index():
    print(request.args)
    return 'Hello Index val: ' + request.args.get("name")


# 默认是get请求，若需要使用post方法，需要显式的配置post
@app.route('/post', methods=['POST'])
def hello_post():
    print(request.data)
    return 'Hello Post val: ' + str(request.data)


# API统一返回数据结构
def response(code: int, message: str, data: any = None):
    body = {'code': code, 'message': message, 'data': {}}
    if data is not None:
        if hasattr(data, '__dict__'):
            body['data'] = data.__dict__
        else:
            body['data'] = data
    return make_response(json.dumps(body, sort_keys=True, ensure_ascii=False), 200)


# 登录接口
# param {"name":"admin","password":"1234"}
@app.route('/login', methods=['POST'])
def login():
    param = json.loads(request.data)
    if "name" not in param:
        return response(1000, "请输入账号")
    if "password" not in param:
        return response(1001, "请输入密码")

    # 通过输入的账号查询数据库是否有这个账号，如果没有则报错
    sql = "SELECT * FROM `teachers` WHERE name=:name"
    ret = query(sql, {"name": param["name"]})

    if len(ret) > 0 and ret[0]["password"] == param["password"]:
        resp = response(0, "登录成功", {"id": ret[0]["id"], "name": ret[0]["name"]})
        resp.set_cookie("id", str(ret[0]["id"]), max_age=3600)
        return resp
    return response(1002, "账号或密码不正确")


# 登出接口
@app.route('/logout', methods=['POST'])
def logout():
    resp = response(0, "退出成功")
    resp.delete_cookie("id")
    return resp


# 通用方法，在数组里查找id匹配的数据
def find_data_by_id(list, id):
    for i in range(len(list)):
        if list[i]['id'] == id:
            return list[i]
    return None


# 通用方法，在数组里删除id匹配的数据
def update_data_by_id(list, id, data):
    for i in range(len(list)):
        if list[i]['id'] == id:
            list[i] = data
            return
    return


# 通用方法，在数组里删除id匹配的数据
def del_data_by_id(list, id):
    for i in range(len(list)):
        if list[i]['id'] == id:
            del(list[i])
            return
    return


# 教师临时数据
# 数据结构{"id":1, "name": '王老师', "password":"1234"}
# teachers = [{"id": 1, "name": 'admin', "password": "1234"}]
# teacherNo = 0


# 教师列表接口
@app.route('/teacher_list', methods=['GET'])
def teacher_list():
    data = []

    sql = "SELECT * FROM `teachers`"
    rets = query(sql)
    if len(rets) > 0:
        for idx, row in enumerate(rets):
            data.append({"id": row["id"], "name": row["name"]})
    return response(0, "ok", data)


# 教师添加接口
# param {"name": '王老师', "password":"1234"}
@app.route('/teacher_add', methods=['POST'])
def teacher_add():
    fields = []
    vals = {}

    if str(request.data) == '':
        return response(1, "参数错误")

    param = json.loads(request.data)
    if "name" not in param:
        return response(1, "请输入账号")
    fields.append("name")
    vals["name"] = param["name"]

    if "password" not in param:
        return response(1, "请输入密码")
    fields.append("password")
    vals["password"] = param["password"]

    usql = "SELECT * FROM `teachers` WHERE name=:name"
    rets = query(usql, {"name": param["name"]})
    if len(rets) > 0:
        return response(1, "用户已存在，请更换用户名")

    sql = "INSERT INTO `teachers`(%s) VALUES(:%s)" % (','.join(fields), ",:".join(fields))
    execute(sql, vals)

    return response(0, "添加成功")
# {'campID': '3', 'user': 'dddd', 'stars': 5, 'time': '2023-04-04 13:00:03', 'desc': 'good 33333'}


# 老师删除接口
# param {id:1}
@app.route('/teacher_del', methods=['POST'])
def teacher_del():
    if str(request.data) == '':
        return response(1, "参数错误")

    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "参数错误")

    sql = "DELETE FROM `teachers` WHERE id=:id"
    execute(sql, {"id": param["id"]})

    return response(0, "删除成功")


# 老师修改接口
# param {"id":1, "name": 'admin', "password": '1234'}
@app.route('/teacher_edit', methods=['POST'])
def teacher_edit():
    fields = []
    vals = {}

    if str(request.data) == '':
        return response(1, "参数错误")
    param = json.loads(request.data)

    if "id" not in param:
        return response(1, "参数错误")
    vals["id"] = param["id"]

    # 数据校检-要更新的数据是否存在
    usql = "SELECT * FROM `teachers` WHERE id=:id"
    rets = query(usql, {"id": param["id"]})
    if len(rets) == 0:
        return response(1, "要更新的用户不存在")

    # 数据校检-要更新的账号是否已存在
    nsql = "SELECT * FROM `teachers` WHERE name=:name"
    nrets = query(nsql, {"name": param["name"]})
    if len(nrets) > 0 and nrets[0]['id'] != param["id"]:
        return response(1, "要更新的账号已存在，请检查")

    if "name" in param:
        if param['name'] == '':
            return response(1, "姓名不能为空")
        fields.append("name")
        vals["name"] = param["name"]

    if "password" in param:
        if param['password'] == '':
            return response(1, "密码不能为空")
        fields.append("password")
        vals["password"] = param["password"]

    # fields => ["name", "password"]
    # %s => name=:name, password=:password
    sets = []
    [sets.append("%s=:%s" % (field, field)) for field in fields]

    sql = "UPDATE `teachers` SET %s WHERE id=:id" % (','.join(sets))
    execute(sql, vals)
    return response(0, "更新成功")


# 学生临时数据
# 数据结构{"id":1, "name": '小王', "english": '12', "chinese": '12', "math": '12'}
students = []
studentNo = 0


# 学生列表接口
@app.route('/student_list', methods=['GET'])
def student_list():
    data = []

    sql = "SELECT * FROM `students`"
    rets = query(sql)
    if len(rets) > 0:
        for idx, row in enumerate(rets):
            print(row)
            data.append({
                "id": row["id"],
                "name": row["name"],
                "english": float(row["english"]),
                "chinese": float(row["chinese"]),
                "math": float(row["math"]),
            })
    return response(0, "ok", data)


# 学生添加接口
# param {"name": '小王', "english": '12', "chinese": '12', "math": '12'}
@app.route('/student_add', methods=['POST'])
def student_add():
    fields = []
    vals = {}

    if str(request.data) == '':
        return response(1, "参数错误")

    param = json.loads(request.data)
    if "name" not in param:
        return response(1, "请输入姓名")
    fields.append("name")
    vals["name"] = param["name"]

    usql = "SELECT * FROM `students` WHERE name=:name"
    rets = query(usql, {"name": param["name"]})
    if len(rets) > 0:
        return response(1, "学生姓名已存在，请重新检查")

    if "english" in param:
        fields.append("english")
        vals["english"] = float(param["english"])
    if "chinese" in param:
        fields.append("chinese")
        vals["chinese"] = float(param["chinese"])
    if "math" in param:
        fields.append("math")
        vals["math"] = float(param["math"])

    sql = "INSERT INTO `students`(%s) VALUES(:%s)" % (','.join(fields), ",:".join(fields))
    execute(sql, vals)
    return response(0, "添加成功")


# 学生删除接口
# param {id:1}
@app.route('/student_del', methods=['POST'])
def student_del():
    if str(request.data) == '':
        return response(1, "参数错误")

    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "参数错误")

    sql = "DELETE FROM `students` WHERE id=:id"
    execute(sql, {"id": param["id"]})
    return response(0, "删除成功")


# 学生修改接口
# param {"id":1, "name": '小王', "english": '12', "chinese": '12', "math": '12'}
@app.route('/student_edit', methods=['POST'])
def student_edit():
    fields = []
    vals = {}

    if str(request.data) == '':
        return response(1, "参数错误")

    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "参数错误")
    vals["id"] = param["id"]

    if "name" not in param:
        return response(1, "姓名不能为空")
    fields.append("name")
    vals["name"] = param["name"]

    # 数据校检-要更新的数据是否存在
    usql = "SELECT * FROM `students` WHERE id=:id"
    rets = query(usql, {"id": param["id"]})
    if len(rets) == 0:
        return response(1, "要更新的学生不存在")

    # 数据校检-要更新的姓名是否已存在
    nsql = "SELECT * FROM `students` WHERE name=:name"
    nrets = query(nsql, {"name": param["name"]})
    if len(nrets) > 0 and nrets[0]['id'] != param["id"]:
        return response(1, "要更新的学生姓名已存在，请检查")

    if "english" in param:
        fields.append("english")
        vals["english"] = float(param["english"])
    if "chinese" in param:
        fields.append("chinese")
        vals["chinese"] = float(param["chinese"])
    if "math" in param:
        fields.append("math")
        vals["math"] = float(param["math"])

    # fields => ["name", "english", "chinese", "math"]
    # %s => name=:name, english=:english, chinese=:chinese, math=:math
    sets = []
    [sets.append("%s=:%s" % (field, field)) for field in fields]

    sql = "UPDATE `students` SET %s WHERE id=:id" % (','.join(sets))
    execute(sql, vals)

    return response(0, "更新成功")


if __name__ == '__main__':
    # app.run(port=9000)
    server = pywsgi.WSGIServer(('0.0.0.0', config.getint('server', 'port')), app)
    server.serve_forever()



    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 