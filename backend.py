import requests
from lxml import etree
import re
import execjs


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
    if _get_IMDB(movie) == False:
        print("No result found.")

def _update_mysql():
    a=1

def push_data():
    a=1

def main():
    movie = '碟中谍4 Mission Impossible'
    get_data(movie)
    push_data()

    return 0

main()
