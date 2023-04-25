import requests
from lxml import etree
import time
import random


def get_weather():
    """
    获取今日或明天的昼间天气信息并返回天气预报字符串。
    """
    day = 'null'
    wea = 'null'
    tem = 'null'
    sky = 'null'
    sport = 'null'
    wear = 'null'
    page = requests.get('http://www.weather.com.cn/weather1d/101043800.shtml')
    if page.status_code == 200:
        page.encoding = 'utf-8'
        page_html = etree.HTML(page.text)
        li_nodes = page_html.xpath('//div[@class="t"]/ul[@class="clearfix"]/li')
        for li_node in li_nodes:
            title_list =  li_node.xpath('h1/text()')
            if len(title_list) > 0:
                title_text = title_list[0]
                if (len(title_text) > 3) and (title_text[-3:] == '日白天'):
                    day = title_text.split('日')[0]
                    wea = li_node.xpath('p[@class="wea"]/text()')
                    tem = li_node.xpath('p[@class="tem"]/span/text()')
                    sky = li_node.xpath('div[@class="sky"]/span/text()')
                    if len(wea) > 0:
                        wea = wea[0]
                    if len(tem) > 0:
                        tem = tem[0]
                    if len(sky) > 0:
                        sky = sky[0]
        li_nodes2_pre = page_html.xpath('//div[@class="livezs"]/ul[@class="clearfix"]')
        if len(li_nodes2_pre) > 0:
            li_nodes2_pre = li_nodes2_pre[0]
            li_nodes2 = li_nodes2_pre.xpath('li')
            for li_node in li_nodes2:
                title_list =  li_node.xpath('em/text()')
                if len(title_list) > 0:
                    title_text = title_list[0]
                    if title_text == '运动指数':
                        sport = li_node.xpath('p/text()')
                        if len(sport) > 0:
                            sport = sport[0]
            wear = li_nodes2_pre.xpath('li[@id="chuanyi"]/a/p/text()')
            if len(wear) > 0:
                wear = wear[0]

    time.sleep(3 + random.random())
    page2 = requests.get('http://www.weather.com.cn/weather/101043800.shtml')
    if page2.status_code == 200:
        page2.encoding = 'utf-8'
        page_html = etree.HTML(page2.text)
        li_nodes = page_html.xpath('//div[@id="7d"]/ul[@class="t clearfix"]/li')
        for li_node in li_nodes:
            title_list =  li_node.xpath('h1/text()')
            if len(title_list) > 0:
                title_text = title_list[0]
                if (len(title_text) > 4) and (title_text[-4:] == '（今天）'):
                    day = title_text.split('日')[0]
                    wea2 = li_node.xpath('p[@class="wea"]/text()')
                    tem_h = li_node.xpath('p[@class="tem"]/span/text()')
                    tem_l = li_node.xpath('p[@class="tem"]/i/text()')
                    if len(wea2) > 0:
                        wea = wea2[0]
                    if len(tem_h) > 0:
                        tem = tem_h[0]
                    if len(tem_l) > 0:
                        tem += '/' + tem_l[0].split('℃')[0]
        li_nodes2_pre = page_html.xpath('//div[@class="hide show"]/ul[@class="clearfix"]')
        if len(li_nodes2_pre) > 0:
            li_nodes2_pre = li_nodes2_pre[0]
            li_nodes2 = li_nodes2_pre.xpath('li')
            for li_node in li_nodes2:
                title_list =  li_node.xpath('em/text()')
                if len(title_list) > 0:
                    title_text = title_list[0]
                    if title_text == '运动指数':
                        sport = li_node.xpath('p/text()')
                        if len(sport) > 0:
                            sport = sport[0]
            wear = li_nodes2_pre.xpath('li[@id="chuanyi"]/a/p/text()')
            if len(wear) > 0:
                wear = wear[0]

    if (day == 'null') or ((wea == 'null') and (tem == 'null') and (sky == 'null') and (sport == 'null') and (wear == 'null')):
        print('null')
        return 'null'
    else:
        back = ''
        if day != 'null':
            back += day + '日昼间'
        if wea != 'null':
            back += '，' + wea
        if tem != 'null':
            back += '，气温' + tem + '℃'
        if sky != 'null':
            back += '，' + sky + '。'
        else:
            back += '。'
        if sport != 'null':
            back += sport
        if wear != 'null':
            back += wear
        print(back)
        return back


if __name__ == '__main__':
    get_weather()
