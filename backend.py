import requests
from lxml import etree
import re
import execjs
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import zhihu_oauth

# 读取配置文件config.json（请将config.json.template改为config.json并填写相关配置信息）
conf_f = open("config.json", "r")
conf_str = conf_f.read()
conf_dic = json.loads(conf_str)

# 以下定义您的知乎账号和密码
zhihu_account = conf_dic["zhihu_account"]
zhihu_passwd = conf_dic["zhihu_passwd"]

# Headers for universe browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}


class GetDouban:
    movie=''
    def __init__(self):
        # 获取豆瓣电影的搜索数据
        url = 'https://search.douban.com/movie/subject_search?search_text=' + self.movie + '&cat=1002'
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

        return 1


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

    data = requests.get(url, headers=headers).text
    d_data = etree.HTML(data)
    context_data = d_data.xpath('//*[@id="SearchMain"]/div/div/div/div/div[1]/div/div/div/div[1]/div[1]/h2/a/text()')
    print(context_data)


def _parse_ajax_web():
    url = 'https://www.zhihu.com/api/v4/search_v3?'
    # 请求头信息
    headers = {
        'Cookie': '_zap=286f5743-64cb-4776-848a-88b1f1bb4ab4; _xsrf=K6QRsRCNzMnZXqFgLKAvQNdJRBjG9rJa; d_c0="AABc2JtbqhGPTmFia1khozJNnOWhTwYEyow=|1596270297"; capsion_ticket="2|1:0|10:1596270297|14:capsion_ticket|44:NDZmNDQ0YTNhYzNjNDZmZjg5MjY5MTdhNDRjYTIyODc=|c47cc31b0a2bbd5520aa06b4944ea5a86533fc127414ba247894215abf9a8841"; z_c0="2|1:0|10:1596270306|4:z_c0|92:Mi4xQmF6cEJnQUFBQUFBQUZ6WW0xdXFFU1lBQUFCZ0FsVk40blFTWUFDa1NlajJuUnY2SlRPaG95OHg2QTRlTHVlVzRB|f66801bcc62c8337f2e52487f3525cfee3b36b62b11b32b929546946a748e96b"; tst=r; q_c1=15415c90ff974389b9525534512bf02c|1596625637000|1596625637000; SESSIONID=1Jnnag6oMzo5ctT70eaYheT3HTTk4mImIQrwQ73vWGL; JOID=Ul0TB0MpgaIz5N-3ei0cOUJ2gBBtHcjOUY29ghds_s4Ei6PmTozMgmjp2bZ0k4-WxtSbaHBzdpAIjUAR44-QPEE=; osd=U1AUB0wojKUz6966fS0TOE9xgB9sEM_OXoywhRdj_8MDi6znQ4vMjWnk3rZ7koKRxtuaZXdzeZEFikAe4oKXPE4=; KLBRSID=9d75f80756f65c61b0a50d80b4ca9b13|1596869983|1596869793',
        'Host': 'www.zhihu.com',
        'Referer': 'http://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept-Encoding': 'gzip',
        'refer': 'https://www.zhihu.com/search?type=content&q=%E7%A2%9F%E4%B8%AD%E8%B0%8D4',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-ab-param': 'li_svip_tab_search=1;li_pl_xj=0;li_panswer_topic=0;se_v_v005=0;top_quality=0;zr_intervene=0;se_vbert3=0;tp_club_feed=0;se_major=0;se_return_1=0;se_hi_trunc=0;se_zp_boost=1;se_v054=0;se_v058=0;ls_fmp4=0;zr_search_paid=1;se_major_v2=0;tp_m_intro_re_topic=1;pf_foltopic_usernum=50;li_viptab_name=0;se_topicfeed=0;se_adsrank=4;se_auth_src=1;tp_fenqu_wei=0;se_videobox=2;se_v_v006=0;se_club_ui=0;soc_feed_intelligent=3;tp_header_style=1;ls_videoad=2;tp_club__entrance2=1;tsp_ios_cardredesign=0;li_sp_mqbk=0;zr_topic_rpc=0;se_preset=0;top_test_4_liguangyi=1;ug_follow_topic_1=2;li_answer_card=0;zw_sameq_sorce=995;zr_rerank=0;tp_club_bt=0;top_universalebook=1;li_yxzl_new_style_a=1;se_ffzx_jushen1=0;se_v057=0;tp_club_fdv4=0;tp_club_entrance=1;se_sug_dnn=1;tp_contents=1;tp_sft=a;li_car_meta=1;li_edu_page=old;zr_training_boost=false;zr_training_first=false;se_entity22=1;se_auth_src2=0;qap_labeltype=1;zr_slotpaidexp=8;se_aa_base=0;tp_meta_card=0;tp_clubhyb=0;zr_slot_training=2;li_yxxq_aut=A1;zr_rec_answer_cp=open;soc_notification=1;ls_recommend_test=0;se_wil_act=0;tsp_ad_cardredesign=0;pf_fuceng=1;ls_video_commercial=0;li_video_section=1;se_college=default;tp_club_top=0;li_vip_verti_search=0;qap_question_author=0;se_usercard=0;top_ebook=0;top_root=0;zr_sim3=0;tp_club_qa_entrance=1;tp_topic_style=0;tp_zrec=1;li_topics_search=0;li_ebook_gen_search=2;se_click_v_v=1;tp_dingyue_video=0;qap_question_visitor= 0;se_t2sug=1;se_mobilecard=0;se_merge=0;tsp_ioscard2=0;pf_newguide_vertical=0;li_paid_answer_exp=0;zr_expslotpaid=1;se_searchwiki=0;se_sug_term=0;pf_creator_card=1;pf_profile2_tab=0;pf_noti_entry_num=2;ug_newtag=1;tp_discover=1;tsp_adcard2=0;zr_search_sim2=2;se_col_boost=1;tp_topic_tab_new=0-0-0;tp_flow_ctr=0;top_v_album=1;zr_km_answer=open_cvr;se_whitelist=1;se_guess=0;se_recommend=0;tsp_hotlist_ui=3;pf_adjust=1;li_svip_cardshow=1;li_catalog_card=1;se_colorfultab=1;se_v053=1;tp_topic_tab=0',
        'x-ab-pb': 'Cg6hCpsKnQqcCicKtAolChIHAAAAAAYABQ==',
        'x-api-version': '3.0.91',
        'x-app-za': 'OS=Web',
        'x-request-with': 'fetch',
        'x-zse-83': '3_2.0',
        'x-zse-86': '1.0_a_xqFU9860tYUGtqKH28kH9ynUYxr_xyBTF0grXye0tY'
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        # "Connection": "keep-alive",
        # "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        # "Accept-Language": "zh-CN,zh;q=0.8",
        # "referer": "https://www.zhihu.com/",
        # 'x-requested-with': 'XMLHttpRequest'
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
    # for item in data:
    #    if item.get('title') is not None:
    #        print(item.get('title'))


def _zhihu_login():
    driver = webdriver.Chrome('./chromedriver')  # 需要修改webdriver的路径
    driver.get("http://www.zhihu.com/#signin")

    elem = driver.find_element_by_name("username")  # 寻找账号输入框
    elem.clear()
    elem.send_keys(zhihu_account)  # 需要修改为你的帐号
    password = driver.find_element_by_name("password")  # 寻找密码输入框
    password.clear()
    password.send_keys(zhihu_passwd)  # 需要修改为你的密码
    # input('请在网页上点击倒立的文字，完成后回到这里按任意键继续')
    elem.send_keys(Keys.RETURN)  # 模拟按下回车键
    time.sleep(10)  # 这里可以直接sleep，也可以使用等待某个条件出现

    url = 'https://www.zhihu.com/api/v4/search_v3?'
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

    # 请求头信息
    headers = {
        # 'Cookie': "K6QRsRCNzMnZXqFgLKAvQNdJRBjG9rJa",
        'Host': 'www.zhihu.com',
        'Referer': 'http://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept-Encoding': 'gzip'
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        # "Connection": "keep-alive",
        # "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        # "Accept-Language": "zh-CN,zh;q=0.8",
        # "referer": "https://www.zhihu.com/",
        # 'x-requested-with': 'XMLHttpReques
    }
    session = requests.session()

    source = session.get(ajax_url, headers=headers)
    print(source)
    # driver.get(ajax_url, headers=headers)

    # print(driver.page_source)
    driver.quit()


def _get_IMDB(movie):
    url = 'https://www.imdb.com/find?q=' + ''.join(re.findall('[a-zA-Z0-9 ]', movie)) + '&ref_=nv_sr_sm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    data = requests.get(url, headers=headers)
    return type(data)
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
        print('{}:\t{}\t{}分'.format(i, title_data, rank_data))

    return i - 1  # 数值会因为逻辑原因多1


def get_data(movie):
    if _get_zhihu(movie) == False:
        print("No result found.")


def _update_mysql():
    a = 1


def push_data():
    a = 1


def main():
    movie = '碟中谍4 Mission Impossible'
    # get_data(movie)
    # push_data()
    # _parse_ajax_web()
    # _zhihu_login()
    a = GetDouban(movie)


    return 0


main()
