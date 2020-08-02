import requests
from lxml import etree
import re
import execjs
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def _get_douban(movie):
    # 获取豆瓣电影的搜索数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url = 'https://search.douban.com/movie/subject_search?search_text=' + movie + '&cat=1002'
    data = requests.get(url, headers=headers)

    # 解密数据包
    e_data = re.search('window.__DATA__ = "([^"]+)"', data.text).group(1)
    with open('douban_decrypt.js', 'r', encoding='gbk') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
    d_data = ctx.call('decrypt', e_data)

    # 提取数据包中的评分信息和标题信息
    str_data = str(d_data).replace('}', ',')  # 统一rank数值后的格式为','结尾
    rank = re.findall(r'\'value\': (.*?),', str_data)
    title = re.findall(r'\'title\': \'(.*?)\'', str_data)

    for i in range(len(rank)):
        print('{}:\t{}\t{}分'.format(i, title[i], rank[i]))

    # for item in d_data['payload']['items']:
    #    print(item)


def _get_zhihu(movie):
    url = 'https://www.zhihu.com/search?type=content&q=' + movie
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    data=requests.get(url,headers=headers).text
    d_data=etree.HTML(data)
    context_data=d_data.xpath('//*[@id="SearchMain"]/div/div/div/div/div[1]/div/div/div/div[1]/div[1]/h2/a/text()')
    print(context_data)


def _parse_ajax_web():
        url = 'https://www.zhihu.com/api/v4/search_v3?'
        # 请求头信息
        headers = {
            'Cookie': "K6QRsRCNzMnZXqFgLKAvQNdJRBjG9rJa",
            'Host': 'www.zhihu.com',
            'Referer': 'http://www.zhihu.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept-Encoding': 'gzip'
            #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
            #"Connection": "keep-alive",
            #"Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            #"Accept-Language": "zh-CN,zh;q=0.8",
            #"referer": "https://www.zhihu.com/",
            #'x-requested-with': 'XMLHttpRequest'
        }
        # 每个ajax请求要传递的参数
        parm = {
            't': 'general',
            'q': '碟中谍 4',
            'correction': 1,
            'offset': 0,
            'limit': 20,
            'lc_idx': 0,
            'show_all_topics': 0
        }
        # 构造ajax请求url
        ajax_url = url + urlencode(parm)
        # 调用ajax请求
        response = requests.get(ajax_url, headers=headers)
        # ajax请求返回的是json数据，通过调用json()方法得到json数据
        json = response.json()
        data = json.get('wiki_box')
        print(json)
        #for item in data:
        #    if item.get('title') is not None:
        #        print(item.get('title'))


def _zhihu_login():
    driver = webdriver.Chrome('./chromedriver')# 需要修改webdriver的路径
    driver.get("http://www.zhihu.com/#signin")

    elem=driver.find_element_by_name("account")# 寻找账号输入框
    elem.clear()
    elem.send_keys("youraccount")# 需要修改为你的帐号
    password=driver.find_element_by_name("password")# 寻找密码输入框
    password.clear()
    password.send_keys("yourpasswd")# 需要修改为你的密码
    input('请在网页上点击倒立的文字，完成后回到这里按任意键继续')
    elem.send_keys(Keys.RETURN)# 模拟按下回车键
    time.sleep(10)# 这里可以直接sleep，也可以使用等待某个条件出现
    print(driver.page_source)
    driver.quit()


def _get_IMDB(movie):
    url = 'https://www.imdb.com/find?q=' + ''.join(re.findall('[a-zA-Z0-9 ]', movie)) + '&ref_=nv_sr_sm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    data = requests.get(url, headers=headers).text
    d_data = etree.HTML(data)
    for i in range(1, 7):  # IMDB最多只生成6个标题
        title_data = d_data.xpath('//*[@id="main"]/div/div[2]/table/tr[{}]/td[2]/a/text()'.format(i))  # 标题序数(x)=tr[x]
        url_data = d_data.xpath('//*[@id="main"]/div/div[2]/table/tr[{}]/td[2]/a/@href'.format(i))
        if (bool(title_data) == 0 or bool(url_data) == 0):
            if i == 1:
                return False
            break
        url = 'https://www.imdb.com' + ''.join(url_data)
        data = requests.get(url, headers=headers).text
        content_data = etree.HTML(data)
        rank_data = content_data.xpath(
            '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
        print('{}:\t{}\t{}分'.format(i,title_data,rank_data))

    return i - 1  # 数值会因为逻辑原因多1


def get_data(movie):
    if _get_zhihu(movie) == False:
        print("No result found.")

def _update_mysql():
    a=1

def push_data():
    a=1

def main():
    movie = '碟中谍4 Mission Impossible'
    #get_data(movie)
    #push_data()
    _parse_ajax_web()
    return 0

main()
