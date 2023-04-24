import requests
from lxml import etree


def get_weather():
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
        if sport != 'null':
            back += sport
        if wear != 'null':
            back += wear
        print(back)
        return back


if __name__ == '__main__':
    get_weather()
