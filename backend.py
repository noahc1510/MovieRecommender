import requests
from lxml import etree
import re
import execjs


def get_douban(movie):
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
    rank = re.findall(r'\'value\': (.*?),', str(d_data).replace('}', ','))
    title = re.findall(r'\'title\': \'(.*?)\'', str(d_data).replace('}', ','))

    for i in range(len(rank)):
        print('{}:\t{}\t{}分'.format(i, title[i], rank[i]))

    # for item in d_data['payload']['items']:
    #    print(item)
    # dd_data = etree.HTML(d_data)
    # name = d_data.xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/span[2]/text()')
    # name=d_data.xpath('//*[@id="content"]/h1/span[1]/text()')
    # print(name)


def main():
    movie = '碟中谍4'
    get_douban(movie)
    print("here")


main()
