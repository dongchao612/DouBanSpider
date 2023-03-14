import re

''''
.       单个字符
[]      字符集，对每一个字符给出取值范围    [abc]表示a、b、c，[a-z]表示a到z单个字符
[^ ]    非字符集，对单个字符给出排除范围    [^abc]表示非a或非b或^c
*       前一个字符的0次或者无数次扩展      abc*表示ab、abc、abcc、abccc等
+       前一个字符的1次或者无数次扩展      abc+表示abc、abcc、abccc等
？      前一个字符的0次或者1次扩展        abc?表示ab、abc
|       左右表达式任意一个               abc|def表示abc或者def


{m}     扩展前一个字符m次       ab{2}c表示  abbc
{m,n}   扩展前一个字符m次到n此       ab{1，2}c表示abc  abbc 
^       匹配字符串开头         ^abc表示abc且在一个字符串开头
$       匹配字符串结尾         ^abc表示abc且在一个字符串结尾
()      分组标记，内部只能用|操作符  (abc)表示abc，(abc|def)表示 abc、def
\d      数字，等价与[0-9]
\w      单词字符，等价于[A-Za-z0-9_]
'''

# 创建模式对象
pat = re.compile("AA")  # 此出的AA，是正则表达式，用来去验证其他的字符串
# search字符串被校验的内容，进行比对查找
# m = pat.search("CBA")  # None
# m = pat.search("ABCAA")  # <re.Match object; span=(3, 5), match='AA'>
# m = pat.search("AABCAADDCCAAA")  ## <re.Match object; span=(0, 2), match='AA'>


# 没有模式对象
# 前面的字符串是规则（模板），后面的字符串是被校验的对象
# m = re.search("AA","Aasd")    #<re.Match object; span=(1, 4), match='asd'>

# 前面字符串是规则（正则表达式），后面字符串是被校验的字符串
# print(re.findall("a", "ASDaDFGAa"))  # ['a', 'a']
# print(re.findall("[A-Z]", "ASDaDFGAa"))  # ['A', 'S', 'D', 'D', 'F', 'G', 'A']
# print(re.findall("[A-Z]+", "ASDaDFGAa"))  # ['ASD', 'DFGA']


# sub
# 找到a用A替换，在第三个字符串中查找"A"
#print(re.sub("a", "A", "abcdcasd"))  # AbcdcAsd

# 建议在正则表达式中，被比较的字符串前面加上r，不用担心转义字符的问题
#a = r"\aabd-\'"
#print(a)

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