import json
import math
from datetime import datetime
from App import db
from flask import Response, request, make_response, url_for, redirect, abort, render_template, session, jsonify
from App.models import User,Order
from . import user_blue
from App import db,cache

@user_blue.route('/')
def getuser():
    return "这是用户模块的首页"

#插入数据
@user_blue.route('/setdata/',methods=['get','post'])
def setdata():
    user = User()
    #dict可以获取user类当中的所有属性 print(user.__dict__)
    user.name = 'Jack'
    user.idcard = '123456789123456789'
    user.sex = '男'

    #事物 Flask默认使用事物
    print(user.__dict__)

    #提交事物使用的是session（sqlalchemy当中的session，并不是服务器中的session）
    try:
        db.session().add(user)
        db.session().commit()
        res = '插入成功'
    except Exception as e:
        print(e)
        db.session.rollback()
        res = '插入失败'

    return res


#触发器 先生成uid再导入到order表  trigger
@user_blue.route('/insert/',methods=['get','post'])
def insert():
    user = User()
    order = Order()
    #dict可以获取user类当中的所有属性 print(user.__dict__)
    user.name = request.args.get('name')
    user.idcard = request.args.get('idcard')
    user.sex = request.args.get('sex')

    #Flask进行插入时默认使用事物,事先读取文件id记录
    db.session().add(user)
    db.session.flush()
    order.uid = user.uid
    order.brand = request.args.get('brand')
    order.ctype = request.args.get('ctype')
    order.price = request.args.get('price')
    order.by_at = datetime.now()

    #提交事物使用的是session（sqlalchemy当中的session，并不是服务器中的session）
    try:
        db.session().add(user)
        db.session().add(order)
        db.session().commit()
        res = {"code":200,"content":"插入成功"}
    except Exception as e:
        print(e)
        db.session.rollback()
        res = {"code":500,"content":"插入失败"}
    return jsonify(res)

#关联查询 inner join（内）  left join（外） / cross join（交叉连接形成笛卡尔积)  /natural join(自然连接 自动寻找关联字段，依据同名字段 效率低 很偷懒)

#cross join
@user_blue.route('/cross/',methods=['get','post'])
def cross():
    res = db.session.query(User)
    print(type(res))
    print(list(res))
    return 'ok'

#inner join
@user_blue.route('/inner/',methods=['get','post'])
def inner():
    #join的第一个参数是主表的名称,第二个参数是指定关联字段
    #select * from user join order on user.uid = order.uid where
    res = db.session.query(User,Order).join(User,User.uid==Order.uid).filter(User.sex.__eq__('男')).order_by(-Order.price)
    list_ = list()
    for tup in res:
        dict_ = dict()
        for obj in tup:
            val = obj.__dict__
            val.pop('_sa_instance_state')
            dict_.update(val)
        list_.append(dict_)
    return jsonify(list_)
    
@user_blue.route('/outer/',methods=['get','post'])
def outer():
    #先查询Order 再看User
    #res = db.session.query(User, Order).join(User, User.uid == Order.uid).filter(User.sex.__eq__('男')).order_by(
     #   -Order.price)
    left = request.args.get('left')
    right = request.args.get('right')
    action = request.args.get('action')
    lf = request.args.get('lf')
    rf = request.args.get('rf')
    res =db.session.execute(f"select * from `{left}` {action} join `{right}` on `{left}`.`{lf}` = `{right}`.`{rf}`")
    #先检查是否为可迭代对象
    userkey = list()
    orderkey = list()
    for k in User.__dict__.keys():
        if '_' not in k and k != '_sa_class_manager':
            userkey.append(k)

    for k in Order.__dict__.keys():
        if '_' not in k and k != '_sa_class_manager':
            orderkey.append(k)

    keys = userkey + orderkey

    #合成字典
    list_ = list()
    for obj in res:
        dict_ = dict()
        for i in range(len(keys)):
            dict_[keys[i]] = obj[i]
        list_.append(dict_)
    return jsonify(list_)

#分页
@user_blue.route('/pageinit/',methods=['get','post'])
@cache.cached(timeout=60)
def pageinit():
    #1 显示第一页
    try:
        page = int(request.args.get('page'))
    except Exception as e:
        page = 1

    #获取最大页码  统计数据量
    count = db.session.query(User,Order).join(User,User.uid==Order.uid).count()



    #select * from tablename where name='张三' limit6,5
    # mongodb    db.tablename.find({name:‘张三’}).skip(6).limit(5)

    #每页展示5条
    num = 5

    end = math.ceil(count / num)
    #page = 1

    #页码判断
    if page < 1:
        page = 1
    elif page > end:
        page = end

    skip = (page-1)*num

    res= db.session.query(User,Order).join(User,User.uid==Order.uid).order_by(-Order.price).offset(skip).limit(num)

    list_ = list()
    for obj in res:
        dict_ = dict()
        for i in range(len(keys)):
            dict_[keys[i]] = obj[i]
        list_.append(dict_)

    return render_template('pageinit.html',set=list_,end=end,page=page)

#　缓存　　cache  保存数据在内存中，预先计算　用空间去换时间
#RESTful 代码架构风格　要求get请求返回的结果和post返回结果不一样 ,接受参数也可以不一致
#   if request.method == 'GET':
#       return A
#elif: request.method == 'PUT':
#........

#pip install flask_restful  是一个类
#flask_restful 通常不写在views中,不太支持html,最适合json


#获取所有数据
@user_blue.route('/getdata/',methods=['get','post'])
def getdata():
    #使用session
    res = db.session().query(User).all()

    #保存过滤后的数据
    resList = list()

    for obj in res:
        dobj = obj.__dict__
        dobj.pop('_sa_instance_state')
        resList.append(dobj)
    return jsonify(resList)



#查询语句 where得到BaseQuery类型
@user_blue.route('/getwhere/',methods=['get','post'])
def getwhere():
    res = db.session().query(User).filter(User.uid > 0)
    resList = list()
    for uobj in list(res):
        dobj = uobj.__dict__
        dobj.pop('_sa_instance_state')
        resList.append(dobj)
    return jsonify(resList)

@user_blue.route('/getone/',methods=['get','post'])
def getone():
    res = db.session().query(User).get(1)
    dobj = res.__dict__
    dobj.pop('_sa_instance_state')
    return dobj

#sqlalchemy使用python魔法方法
@user_blue.route('/getfilter/',methods=['get','post'])
def getfilter():
    '''
    __le__()   <=
    __ge__()   >=
    __gt__()   >
    __eq__()   ==
     '''

    res = db.session().query(User.uid.__eq__(1))
    return jsonify(list(res[0].__dict__))

#修改
@user_blue.route('/update/',methods=['get','post'])
def update():
    #先查询，把原数据覆盖
    user = db.session.query(User).get(1)
    user.name = '赵四'
    #提交
    db.session.add(user)
    db.session.commit()
    return 'ok'

#删除
@user_blue.route('/drop/',methods=['get','post'])
def drop():
    #先查询，把原数据覆盖
    users = db.session.query(User).filter()
    for obj in users:
        db.session.delete(obj)
    db.session.commit()
    return 'ok'

#like
@user_blue.route('/wherelike/',methods=['get','post'])
def wherelike():
    #startswith 以什么什么开头
    #...startswith/endswith
    res = db.session.query(User).filter(User.name.startswith('J'))
    listRes = list()
    for obj in res:
        dobj = obj.__dict__
        dobj.pop('_sa_instance_state')
        listRes.append(dobj)

    return jsonify(listRes)

#in/notin
# @user_blue.route('/wherein/',methods=['get','post'])
# def wherein():
#     res = db.session.query(User).filter(User.uid.in_([0,4])
#     return 'ok'


@user_blue.route('/getjson/', methods=['get', 'post'])
def getjson():
    keys = ['name', 'age']
    values = ['tom', 18]
    d = dict(zip(keys, values))
    str_ = Response(json.dumps(d), content_type='application/json', )
    return 'str_'


# Request 请求对象
@user_blue.route('/testreq/',methods=['get','post'])
def testreq():
# '''
# RESTFUL 知道对方的请求方式，get请求返回A，post返回
# 统计分析 服务器哪个接口被访问的次数最多
# 爬虫 记录ip，统计时间
#
# '''

# 请求方式
# return str(request.method)
# 完整路径
# return str(request.base_url)
# 主机地址
# return str(request.host_url)
# 请求路径
    #return str(request.path)
# 请求时间

    #return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# 用集合收取ip地址
    #return str(request.remote_addr)

# 使用request获取参数
    @user_blue.route('/getparams/',methods=['get','post'])
    def getparams():
    # 获取传递参数的key   dict.get('key',None)
    # 在url的传递中，所有的值都是str
        name = request.args.get('name')
    # from是在表单提交时使用的
        age = request.form.get('age', None)
        return name + str(age)


# 获取请求头
@user_blue.route('/getheaders/', methods=['get', 'post'])
def getheaders():
    ip = str(request.remote_addr)
    head = str(request.headers)
    return ip + ':' + head


# Flask 自带的微型服务器垃圾  推荐用nginx+uwsgi

# response响应对象
@user_blue.route('/getres/', methods=['get', 'post'])
def getres():
    name = request.args.get('name')
    result = make_response(f"<h1>{name}立刻还花呗</h1>")
    return result


# 重定向
# 猜想： 登录：表单-->验证的接口--> 跳转
@user_blue.route('/redirect_/', methods=['get', 'post'])
def redirect_():
    # 反向解析 url_for("user.getres")
    path = url_for("user.getres")
    # rediect是一个response对象
    # 跳转
    rep = redirect(f"{path}?name=李宗大")
    print(type(rep))
    return rep


# 最后一种Response对象
@user_blue.route('/respon/', methods=['get', 'post'])
def respon():
    res = Response("您好!帅气的李宗大！")
    print(type(res))
    return res


# 异常处理
# 某一个接口并不想被直接请求，只要是get就跳转
# delete 删除 --> 汇款
@user_blue.route('/abort_/', methods=['get', 'delete'])
def abort_():
    # abort并不能抛出一个自定义错误
    if request.method == 'GET':
        abort(404)
    elif request.method == 'DELETE':
        pass

    return 'error404'


# errorhandler的值是一个错误编码
@user_blue.errorhandler(404)
def errhand(exception):
    # 该函数的意义是如果得到了404，默认怎么处理
    red = redirect('http://www.baidu.com')
    return red


# cookie 和 session
# cookie 和 session：都是会话技术
# cookie存储在浏览器端    SQLlite --> 手机存储淘宝
# session存储在服务端  数据库  SQL NoSQL
# 服务器在登录之前是不会记录状态的；传递账号密码-->服务器验证id-->服务器保存id-->服务器吧sessionid传递给浏览器，浏览器用cookie保存sessionid


# 登录
@user_blue.route("/loginaction/")
def loginaction():
    account = request.args.get('account')
    pwd = request.args.get('pwd', '')
    red = redirect('/u/tosessionindex/')

    # 设置cookie response对象中进行的设置
    #red.set_cookie('user', account)

    #设置session,redis可以利用内存
    session['user'] = account
    return red

#Flask session -> 配置redis -> 读取session配置 -> app(Flask) -> 将session和flask关联 ->ok
#在Flask中，浏览器退出，存储sessionkey的cookie默认被清除
@user_blue.route("/tosessionindex/")
#redis只存储5秒（不进硬盘），登录用户很多，如何解决session内存不足的情况？（专门架设一个redis服务器）
def tosessionindex():
    # 服务器获取cookie 浏览器用request
    #cookie不可以跨浏览器使用,给每个浏览器的存储是独立的
    #account = request.cookies.get("user", '游客李晶晶')
    account = session.get("user",'游客')
    # 读取html
    return render_template('hlm.html',account=account)

#面试题：主从延迟如何解决
#bin-log：主机器写入以后 产生日志 -->发送给服务器 -->从机器去主机器拷贝数据 --> 将读过来的数据进行写入
#提升‘带宽’ = 降低使用量  1主连3-5从 --> 从再连从服务器
#主从  可以做读写分离   备份    从服务器选择read-only

@user_blue.route('/up/')
def up():
    return render_template('up.html')