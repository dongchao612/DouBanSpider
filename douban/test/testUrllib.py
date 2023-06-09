import urllib.request

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# 获取一个get请求
response = urllib.request.urlopen("http://www.baidu.com")
print(response.read().decode("utf-8"))#对获取到的网页源码进行utf-8解码

# 获取一个post请求
# import urllib.parse
# data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response = urllib.request.urlopen("http://www.httpbin.org/post",data=data)
# print(response.read().decode("utf-8"))


# 超时处理
# import urllib.error
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get", timeout=0.01)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as e:
#     print("time out!")

# response详情
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.status)
# print(response.getheaders())
# print(response.getheader("Server"))

# headers
# import urllib.parse
# url = "http://httpbin.org/post"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
# }
# data = bytes(urllib.parse.urlencode({'name': 'eric'}), encoding="utf-8")
# req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
# response = urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
}
req = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
