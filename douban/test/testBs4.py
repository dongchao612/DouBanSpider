from bs4 import BeautifulSoup

'''
BeautifulSoup4将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:

- Tag
- NavigableString
- BeautifulSoup
- Comment
'''

file = open("baidu.html", "rb")
html = file.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")

# 1.Tag  标签及其内容；拿到它所找到的第一个内容
# print(bs.title)
'''
<title>百度一下，你就知道 </title>
'''

# print(bs.a)
'''
<a class="mnav" href="http://news.baidu.com" name="tj_trnews"><!--新闻--></a>
'''

# print(bs.head)# <head>...</head>


# print(type(bs.head))  # <class 'bs4.element.Tag'>

# 2.NavigableString  标签里的内容（字符串)
# print(bs.title.string)
'''
百度一下，你就知道
'''

# print(type(bs.title.string))# <class 'bs4.element.NavigableString'>

# print(bs.a.attrs)#拿到标签的属性
'''
{'class': ['mnav'], 'href': 'http://news.baidu.com', 'name': 'tj_trnews'}
'''

# 3.BeautifulSoup   表示整个文档
# print(type(bs))# <class 'bs4.BeautifulSoup'>

# print(bs.name)# [document]

# print(bs)# <!DOCTYPE html>...</html>


# 4.Comment  是一个特殊的NavigableString ，输出的内容不包含注释符号
# print(bs.a.string)
'''
新闻
'''
# print(type(bs.a.string))  # <class 'bs4.element.Comment'


# -------------------------------

# 文档的遍历

# print(bs.head.contents)
# print(bs.head.contents[1])

# 文档的搜索

# (1)find_all()
# 字符串过滤：会查找与字符串完全匹配的内容
# t_list = bs.find_all("a")
'''
[<a class="mnav" href="http://news.baidu.com" name="tj_trnews"><!--新闻--></a>, <a class="mnav" href="http://news.baidu.com" name="tj_trnews">新闻</a>, <a class="mnav" href="https://www.hao123.com" name="tj_trhao123">hao123</a>, <a class="mnav" href="http://map.baidu.com" name="tj_trmap">地图</a>, <a class="mnav" href="http://v.baidu.com" name="tj_trvideo">视频</a>, <a class="mnav" href="http://tieba.baidu.com" name="tj_trtieba">贴吧</a>, <a class="bri" href="//www.baidu.com/more/" name="tj_briicon" style="display: block;">更多产品 </a>]
'''
import re

# 正则表达式搜索：使用search（）方法来匹配内容
# t_list = bs.find_all(re.compile("a"))#只要包含就会有
'''
[<head>
<meta content="text/html;charset=utf-8" http-equiv="content-type"/>
<meta content="IE=Edge" http-equiv="X-UA-Compatible"/>
<meta content="always" name="referrer"/>
<link href="https://ss1.bdstatic.com/5eN1bjq8AAUYm2zgoY3K/r/www/cache/bdorz/baidu.min.css" rel="stylesheet" type="text/css"/>
<title>百度一下，你就知道 </title>
</head>, <meta content="text/html;charset=utf-8" http-equiv="content-type"/>, <meta content="IE=Edge" http-equiv="X-UA-Compatible"/>, <meta content="always" name="referrer"/>, <a class="mnav" href="http://news.baidu.com" name="tj_trnews"><!--新闻--></a>, <a class="mnav" href="http://news.baidu.com" name="tj_trnews">新闻</a>, <a class="mnav" href="https://www.hao123.com" name="tj_trhao123">hao123</a>, <a class="mnav" href="http://map.baidu.com" name="tj_trmap">地图</a>, <a class="mnav" href="http://v.baidu.com" name="tj_trvideo">视频</a>, <a class="mnav" href="http://tieba.baidu.com" name="tj_trtieba">贴吧</a>, <a class="bri" href="//www.baidu.com/more/" name="tj_briicon" style="display: block;">更多产品 </a>]
'''

# 方法  ： 传入一个函数（方法),根据函数的要求来搜索  (了解）
# def name_is_exists(tag):
#     return tag.has_attr("name")
#
#
# t_list = bs.find_all(name_is_exists)
# for item in t_list:
#     print(item)

# 2.kwargs   参数
# t_list= bs.find_all(id="head")
# t_list = bs.find_all(href="http://news.baidu.com")
# t_list = bs.find_all(class_=True)


# 3.text参数
# t_list= bs.find_all(text = "hao123")
# t_list = bs.find_all(text =["hao123","地图","贴吧"])

# t_list = bs.find_all(text=re.compile("\d"))  # 应用正则表达式来查找包含特定文本的内容（标签里的字符串）

# 4.limit 参数
# t_list = bs.find_all("a",limit=3)

t_list = bs.select('title')  # 通过标签来查找
t_list = bs.select(".mnav")  # 通过类名来查找
t_list = bs.select("#u1")  # 通过id来查找
t_list = bs.select("a[class='bri']")  # 通过属性来查找
t_list = bs.select("head > title")  # 通过子标签来查找
t_list = bs.select(".mnav ~ .bri")
t_list = bs.select("div[id='u1'] > a[class='mnav']")
for item in t_list:
    print(item)
