import sqlite3

# 1.连接数据库
# conn = sqlite3.connect("test.db") #打开或创建数据库文件
# if conn:
#     print("Opened database successfully")

# 2.创建数据表
# conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
# if conn:
#     print("成功打开数据库")
# c = conn.cursor()  # 获取游标
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real);'''
# c.execute(sql)  # 执行sql语句
# conn.commit()  # 提交数据库操作
# conn.close()  # 关闭数据库连接
# print("成功建表")

# 3.插入数据
# conn = sqlite3.connect("test.db")       #打开或创建数据库文件
# if conn:
#     print("成功打开数据库")
# c = conn.cursor()       #获取游标
# sql1 = '''
#    insert into company (id,name,age,address,salary)
#     values (1,'张三',32,"成都",8000);
# '''
# c.execute(sql1)          #执行sql语句
# sql2 = '''
#    insert into company (id,name,age,address,salary)
#     values (2,'李四',30,"重庆",15000);
# '''
# c.execute(sql2)          #执行sql语句
# conn.commit()
# conn.close()            #关闭数据库连接
#
# print("插入数据完毕")

# 4.查询数据
conn = sqlite3.connect("test.db")  # 打开或创建数据库文件
print("成功打开数据库")
c = conn.cursor()  # 获取游标
sql = "select id,name,address,salary from company"
cursor = c.execute(sql)  # 执行sql语句 <class 'sqlite3.Cursor'>
for row in cursor:
    print("id = ", row[0], "name = ", row[1], "address = ", row[2], "salary = ", row[3])
conn.close()  # 关闭数据库连接
print("查询完毕")
