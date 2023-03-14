# DouBanSpider
爬取豆瓣电影TOP250，并利用flask框架进行可视化
## 技术分析

### testUrllib
```python
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_con
```
####  获取一个get请求
```python
response = urllib.request.urlopen("http://www.baidu.com")
print(response.read().decode("utf-8"))#对获取到的网页源码进行utf-8解码
```
#### 获取一个post请求
```python
import urllib.parse
data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
response = urllib.request.urlopen("http://www.httpbin.org/post",data=data)
print(response.read().decode("utf-8"))
```

#### 超时处理
```python
try:
     response = urllib.request.urlopen("http://httpbin.org/get", timeout=0.01)
     print(response.read().decode("utf-8"))
except urllib.error.URLError as e:
     print("time out!")
```
#### response详情

```python
 response = urllib.request.urlopen("http://www.baidu.com")
# print(response.status)
# print(response.getheaders())
# print(response.getheader("Server"))
```
#### headers伪装
```python
import urllib.parse
url = "http://httpbin.org/post"
headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
data = bytes(urllib.parse.urlencode({'name': 'eric'}), encoding="utf-8")
req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
```

#### 测试
```python
url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
}
req = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
```

### testBs4
```python
from bs4 import BeautifulSoup
```
```html
<!DOCTYPE html>
<html>
<head>
    <meta content="text/html;charset=utf-8" http-equiv="content-type" />
    <meta content="IE=Edge" http-equiv="X-UA-Compatible" />
    <meta content="always" name="referrer" />
    <link href="https://ss1.bdstatic.com/5eN1bjq8AAUYm2zgoY3K/r/www/cache/bdorz/baidu.min.css" rel="stylesheet" type="text/css" />
    <title>百度一下，你就知道 </title>
</head>
<body link="#0000cc">
  <div id="wrapper">
    <div id="head">
        <div class="head_wrapper">
          <div id="u1">
            <a class="mnav" href="http://news.baidu.com" name="tj_trnews"><!--新闻--></a>
            <a class="mnav" href="http://news.baidu.com" name="tj_trnews">新闻</a>
            <a class="mnav" href="https://www.hao123.com" name="tj_trhao123">hao123</a>
            <a class="mnav" href="http://map.baidu.com" name="tj_trmap">地图</a>
            <a class="mnav" href="http://v.baidu.com" name="tj_trvideo">视频</a>
            <a class="mnav" href="http://tieba.baidu.com" name="tj_trtieba">贴吧</a>
            <a class="bri" href="//www.baidu.com/more/" name="tj_briicon" style="display: block;">更多产品 </a>
          </div>
        </div>
    </div>
  </div>
</body>
</html>
```
#### Tag  标签及其内容；拿到它所找到的第一个内容
```python
file = open("baidu.html", "rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")

print(bs.title) # <title>百度一下，你就知道 </title>

print(bs.a) # <a class="mnav" href="http://news.baidu.com" name="tj_trnews"><!--新闻--></a>

print(bs.head)# <head>...</head>


print(type(bs.head))  # <class 'bs4.element.Tag'>
```
#### NavigableString  标签里的内容（字符串)
```python
print(bs.title.string)# 百度一下，你就知道

print(type(bs.title.string))# <class 'bs4.element.NavigableString'>

#拿到标签的属性 
print(bs.a.attrs) # {'class': ['mnav'], 'href': 'http://news.baidu.com', 'name': 'tj_trnews'}
```
#### BeautifulSoup   表示整个文档
```python
print(type(bs))# <class 'bs4.BeautifulSoup'>

print(bs.name) # [document]

print(bs) # <!DOCTYPE html> ...</html>
```
#### Comment  是一个特殊的NavigableString ，输出的内容不包含注释符号
```python
print(bs.a.string)# 新闻

print(type(bs.a.string))  # <class 'bs4.element.Comment'
```
#### 文档的遍历
```python
print(bs.head.contents)
print(bs.head.contents[1])
```
#### 文档的搜索
- (1) find_all() 
```python
# 1、字符串过滤：会查找与字符串完全匹配的内容
t_list = bs.find_all("a")# [<a>...</a>,<a>...</a>,<a>...</a>]

# 2、正则表达式搜索：使用search（）方法来匹配内容
import re
#只要包含就会有 
t_list = bs.find_all(re.compile("a"))# [<head>...</head>,<meta>...</meta>]

# 3、传入一个函数（方法),根据函数的要求来搜索  (了解）
def name_is_exists(tag):
     return tag.has_attr("name")

t_list = bs.find_all(name_is_exists)
for item in t_list:
    print(item)

# 4、kwargs   参数
t_list= bs.find_all(id="head")
t_list = bs.find_all(href="http://news.baidu.com")
t_list = bs.find_all(class_=True)

# 5、text参数
t_list= bs.find_all(text = "hao123")
t_list = bs.find_all(text =["hao123","地图","贴吧"])

t_list = bs.find_all(text=re.compile("\d"))  # 应用正则表达式来查找包含特定文本的内容（标签里的字符串）

# 6、limit 参数
t_list = bs.find_all("a",limit=3)
```
-  (2) select()
```python
t_list = bs.select('title')  # 通过标签来查找
t_list = bs.select(".mnav")  # 通过类名来查找
t_list = bs.select("#u1")  # 通过id来查找
t_list = bs.select("a[class='bri']")  # 通过属性来查找
t_list = bs.select("head > title")  # 通过子标签来查找
t_list = bs.select(".mnav ~ .bri")
t_list = bs.select("div[id='u1'] > a[class='mnav']")
for item in t_list:
    print(item)
```
### testRe
| 符号| 含义|示例 |
|---|---|---|
|. |单个字符 | |
|[]  |字符集，对每一个字符给出取值范围 | [abc]表示a、b、c，[a-z]表示a到z单个字符|
| [^ ]|非字符集，对单个字符给出排除范围 |[^abc]表示非a或非b或^c |
| *| 前一个字符的0次或者无数次扩展 | abc*表示ab、abc、abcc、abccc等|
|+ | 前一个字符的1次或者无数次扩展  | abc+表示abc、abcc、abccc等|
|？ | 前一个字符的0次或者1次扩展 | abc?表示ab、abc|
| \|  左右表达式任意一个 | abc &#x7C; def表示abc或者def|
| {m}     | 扩展前一个字符m次  |      ab{2}c表示  abbc|
|{m,n}  | 扩展前一个字符m次到n此   |      ab{1，2}c表示abc  abbc  |
| ^      |   匹配字符串开头      |     ^abc表示abc且在一个字符串开头 |
| $     |    匹配字符串结尾     |      ^abc表示abc且在一个字符串结尾 |
| ()       | 分组标记，内部只能用|操作符  (abc)表示abc，(abc|def)表示 abc、def |
| \d       | 数字，等价与[0-9] |  |
| \w       | 单词字符，等价于[A-Za-z0-9_] |  |

 #### 创建模式对象
 ```python
import re

pat = re.compile("AA")  # 此出的AA，是正则表达式，用来去验证其他的字符串
# search字符串被校验的内容，进行比对查找
m = pat.search("CBA")  # None
m = pat.search("ABCAA")  # <re.Match object; span=(3, 5), match='AA'>
m = pat.search("AABCAADDCCAAA")  ## <re.Match object; span=(0, 2), match='AA'>
 ```
 #### 没有模式对象
```python
# 前面的字符串是规则（模板），后面的字符串是被校验的对象
m = re.search("AA","Aasd")    #<re.Match object; span=(1, 4), match='asd'>
```
#### 前面字符串是规则（正则表达式），后面字符串是被校验的字符串
```python
print(re.findall("a", "ASDaDFGAa"))  # ['a', 'a']
print(re.findall("[A-Z]", "ASDaDFGAa"))  # ['A', 'S', 'D', 'D', 'F', 'G', 'A']
print(re.findall("[A-Z]+", "ASDaDFGAa"))  # ['ASD', 'DFGA']
```
#### sub
```python
# 找到a用A替换，在第三个字符串中查找"A"
print(re.sub("a", "A", "abcdcasd"))  # AbcdcAsd
```
> 建议在正则表达式中，被比较的字符串前面加上r，不用担心转义字符的问题
```python
a = r"\aabd-\'"
print(a)
```

```python
string='''
        <div class="hd">
            <a class="" href="https://movie.douban.com/subject/1292052/">
            <span class="title">肖申克的救赎</span>
            <span class="title"> / The Shawshank Redemption</span>
            <span class="other"> / 月黑高飞(港)  /  刺激1995(台)</span>
            </a>
            <span class="playable">[可播放]</span>
        </div>
'''
print(re.findall(r'<span(.*)</span>',string))
# [' class="title">肖申克的救赎', ' class="title">\xa0/\xa0The Shawshank Redemption', ' class="other">\xa0/\xa0月黑高飞(港)  /  刺激1995(台)', ' class="playable">[可播放]']
```

### testXlwt

```python
# 示例
import xlwt

workbook = xlwt.Workbook(encoding="utf-8")  #创建workbook对象
worksheet = workbook.add_sheet('sheet1')    #创建工作表

worksheet.write(0,0,'hello')        #写入数据，第一行参数”行“，第二个参数”列“，第三个参数内容
workbook.save('student.xls')        #保存数据表
```

```python
# 将99乘法表写入excel 
workbook = xlwt.Workbook(encoding="utf-8")  #创建workbook对象
worksheet = workbook.add_sheet('sheet1')    #创建工作表
for i in range(0,9):
    for j in range(0,i+1):
        worksheet.write(i,j,"%d * %d = %d "%(i+1,j+1,(i+1)*(j+1)))

workbook.save('student.xls')        #保存数据表
```
### testSqlite3
#### 连接数据库
```python
import sqlite3

conn = sqlite3.connect("test.db") #打开或创建数据库文件
if conn:
     print("Opened database successfully")
```
#### 创建数据表
```python
conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
if conn:
    print("成功打开数据库")
c = conn.cursor()  # 获取游标
sql = '''
    create table company
        (id int primary key not null,
        name text not null,
        age int not null,
        address char(50),
        salary real);'''
c.execute(sql)  # 执行sql语句
conn.commit()  # 提交数据库操作
conn.close()  # 关闭数据库连接
print("成功建表")
```
#### 插入数据
```python
conn = sqlite3.connect("test.db")       #打开或创建数据库文件
if conn:
    print("成功打开数据库")
c = conn.cursor()       #获取游标
sql1 = '''
   insert into company (id,name,age,address,salary)
    values (1,'张三',32,"成都",8000);
'''
c.execute(sql1)          #执行sql语句
sql2 = '''
   insert into company (id,name,age,address,salary)
    values (2,'李四',30,"重庆",15000);
'''
c.execute(sql2)          #执行sql语句
conn.commit()
conn.close()            #关闭数据库连接

print("插入数据完毕")
```
#### 查询数据
```python
conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
print("成功打开数据库")
c = conn.cursor()  # 获取游标
sql = "select id,name,address,salary from company"
cursor = c.execute(sql)  # 执行sql语句 <class 'sqlite3.Cursor'>
for row in cursor:
    print("id = ", row[0], "name = ", row[1], "address = ", row[2], "salary = ", row[3])
conn.close()  # 关闭数据库连接
print("查询完毕")
```

### testFlask

```python
from flask import Flask, render_template, request  # 从flask引入Flask类
import datetime

app = Flask(__name__)  # 初始化对象

# 路由路径[函数名]不能重复，用户通过唯一路径访问特定的函数
if __name__ == '__main__':
    app.run()
```

#### 路由解析

```python
@app.route('/')
def hello_world():
     return '你好，欢迎光临！'

@app.route('/index')
def hello():
    return '你好'
```

#### 通过访问路径，获取用过户字符串参数

```python
@app.route('/user/<name>')
def welcome(name):
    return "你好%s" % name
```

#### 通过访问路径，获取用过户整形参数，此外还有float类型

```python
@app.route('/user/<int:id>')
def welcome2(id):
    return "你好%d" % id + "号的会员"
```

#### 返回给用过户渲染后的文件

```python
@app.route("/")
def index1(): # 需要注释hello_world() 否则不会显示
    return render_template("test.html")
```

#### 向页面传递参数

```python
@app.route("/")
def index2():
    time = datetime.date.today()  # 普通参数
    name = ["小王", "小张", "小航"]
    task = {"任务": "打扫卫生", "时间": "3小时"}
    return render_template("index.html", var=time, list=name, task=task)  # 前者是网页中使用的变量名
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>index</title>
</head>
<body>
    <h1>今天是{{ var }}，欢迎光临</h1>
    <br>
    今天值班的人是：<br><!--用大括号括起来的是控制结构-->
    {% for data in list %}
        <li>{{ data }}</li>
    {% endfor %}

    任务是：<br><!--了解如何在页面打印表格，以及如何迭代-->
    <table border="1">
        {% for key,value in task.items() %}<!-- [(k,v),(k,v))]-->
            <tr>
                <td>{{ key }}</td>
                <td>{{ value }}</td>
            </tr>
        {% endfor %}
    </table>
</body>
</html>
```

#### 如何进行表单提交

```python
@app.route('/register')
def register():
    return render_template("test/register.html")

@app.route("/result", methods=['POST', 'GET'])  # 接受路由必须指定methods
def result():
    if request.method == 'POST':
        result = request.form  # 返回字典，键:name,值：输入的内容
        return render_template("test/result.html", result=result)
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <table border="1">
        {% for key,value in result.items() %}<!-- [(k,v),(k,v))]-->
            <tr>
                <th>{{ key }}</th>
                <td>{{ value }}</td>
            </tr>
        {% endfor %}
</body>
</html>
```

## 具体实现

### 1 爬取网页

### 2 逐一解析数据

### 3 保存数据-Excel

### 4  保存数据-DB