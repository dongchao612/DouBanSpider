from bs4 import BeautifulSoup  # 网页解析
import re  # 正则表达式，进行文字匹配
import xlwt  # 进行excel操作
import urllib.request, urllib.error  # 指定url，获取网页数据
import sqlite3  # 进行数据库操作


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1、爬取网页
    datalist = getData(baseurl)

    # 3、保存数据
    #savepath = "./豆瓣top250.xls"
    #saveData(datalist, savepath)

    dbpath='./豆瓣top250.db'
    saveData2DB(datalist,dbpath)
    # askUrl("https://movie.douban.com/top250?start=0")


# 爬取网页
def getData(baseurl):
    print("开始爬取数据...")
    datalist = []
    for i in range(0, 10):  # 调取获得信息的函数10次
        print(f"\t正在爬取第{i+1}页的信息")
        url = baseurl + str(i * 25)

        # print(url)
        html = askUrl(url)  # 保存获取到的网页源码
        # 2、逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        # print(soup.find_all("div",class_='item').__len__())25
        # print(soup.select("div[class='item']").__len__())25
        for item in soup.find_all("div", class_='item'):
            data = []
            item = str(item)

            # 添加链接
            link = re.findall(r'<a href="(.*?)">', item)[0]
            data.append(link)

            # 添加图片url
            imgSrc = re.findall(r'src="(.*?)"', item)[0]
            data.append(imgSrc)

            # 添加电影名
            titles = re.findall(r'<span class="title">(.*?)</span>', item)  # 片名可能只有一个中文名，没有外国名
            if (len(titles) == 2):
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号
                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名字留空

            # 添加评分
            rating = re.findall(r'<span class="rating_num" property="v:average">(.*)</span>', item)[0]
            data.append(rating)  # 添加评分

            # 添加评分人数
            judgeNum = re.findall(r'<span>(.*?)人评价</span>', item)[0]
            data.append(judgeNum)  # 提加评价人数

            # 添加概况
            inq = re.findall(r'<span class="inq">(.*?)</span>', item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")  # 留空

            # 添加相关信息
            bd = re.findall(r'<p class="">(.*?)</p>', item, re.S)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)  # 把处理好的一部电影信息放入datalist
    print("爬取结束！")
    return datalist


#得到指定一个URL的网页内容
def askUrl(url):
    # 模拟浏览器头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
    }
    request = urllib.request.Request(url=url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request,timeout=1)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 保存数据
def saveData(datalist, savepath):
    print("开始保存....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表

    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名

    for i in range(0, datalist.__len__()):
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)
    print("保存结束！")

def init_db(dbpath):
    sql = '''
        create table movie250 
        (
        id integer PRIMARY KEY  NOT NULL,
        info_link text,
        pic_link text,
        cname varchar(10),
        ename varchar(10),
        score numeric ,
        rated numeric ,
        instroduction text,
        info text
        )

    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveData2DB(datalist,dbpath):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into movie250 (
                    info_link,pic_link,cname,ename,score,rated,instroduction,info)
                values(%s)''' % ",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':  # 当程序执行时
    # 调用函数
    main()
