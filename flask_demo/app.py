from flask import Flask, render_template, request  # 从flask引入Flask类
import datetime

app = Flask(__name__)  # 初始化对象


# 路由解析
# @app.route('/')
# def hello_world():
#     return '你好，欢迎光临！'

@app.route('/index')
def hello():
    return '你好'


# 通过访问路径，获取用过户字符串参数
@app.route('/user/<name>')
def welcome(name):
    return "你好%s" % name


# 通过访问路径，获取用过户整形参数，此外还有float类型
@app.route('/user/<int:id>')
def welcome2(id):
    return "你好%d" % id + "号的会员"


# 返回给用过户渲染后的文件
# @app.route("/")
# def index1():  # 需要注释hello_world(),否则不会显示
#     return render_template("test.html")


# 向页面传递参数
@app.route("/")
def index2():
    time = datetime.date.today()  # 普通参数
    name = ["小王", "小张", "小航"]
    task = {"任务": "打扫卫生", "时间": "3小时"}
    return render_template("index.html", var=time, list=name, task=task)  # 前者是网页中使用的变量名

# 如何进行表单提交
@app.route('/register')
def register():
    return render_template("test/register.html")

@app.route("/result", methods=['POST', 'GET'])  # 接受路由必须指定methods
def result():
    if request.method == 'POST':
        result = request.form  # 返回字典，键:name,值：输入的内容
        return render_template("test/result.html", result=result)


# 路由路径[函数名]不能重复，用户通过唯一路径访问特定的函数
if __name__ == '__main__':
    app.run(debug=True)
