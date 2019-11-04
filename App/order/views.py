import json
import uuid

from . import order_blue
from flask import render_template,url_for



# 模块首页
@order_blue.route('/')
def getorder():
    return render_template('getorder.html')

#传参是要定义参数，方法中要接收参数 Flask支持四种返回类型，字符串，json，tuple，Response（是Flask当中的一个对象）
@order_blue.route('/testid/<int:id>/')
def testid(id):
    print(type(id))
    return '123'

@order_blue.route('/test/<float:id>/')
def test(id):
    print(type(id))
    return str(id)

@order_blue.route('/createuuid/')
def createuuid():
    uid = uuid.uuid4()
    print(uid)
    return str(uid)

@order_blue.route('/testany/<any("女","保密"):sex>/')
def testany(sex):
    print(type(sex))
    return str(sex)

@order_blue.route('/testpath/<string:name>/<path:path>')
def testpath(name,path):
    print(name)
    print(path)
    return name+path
#method是列表，列表中是字符串，代表一种类型的请求
@order_blue.route('/testget1/',methods=['post','get'])
def testget():
    return "get"

#正向解析
#反向解析

@order_blue.route('/inverse/',methods=['post','get'])
def inverse():
    #url_for:'blueprintname,funcname'
    path = url_for("order.testget")
    #path = "/o/testget1"
    return path

#XML
@order_blue.route('/testxml/',methods=['post','get'])
def testxml():
    #长字符串，原样输出
    xml = '''
<root>
    <info>
        <name>赵四</name>
        <age>18</age>
    </info>
    <info>
        <name>宋小宝</name>
        <age>81</age>
    </info>
<root>    
    '''
    return xml

#json
@order_blue.route('/testjson/',methods=['post','get'])
def testjson():
    #元组包裹字典
    global dict
    dict_ = dict(name='赵四',age=18),{"name":'宋小宝',"age":'81'}
    return json.dumps(dict_)

#tuple
@order_blue.route('/testtuple/',methods=['post','get'])
def testtuple():
    str_ = '访问成功'
    return str_,404