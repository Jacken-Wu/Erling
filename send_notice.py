import time
import random
from bot_func.send import *
from bot_func.constant import *
from bot_func.account import view_account
import os
from bot_func.weather import get_weather
from bot_func.biliVideo import BiliScratch, send_video, clean_video_temp


def send_notice(user_id: int):
    """
    @param user_id: int
    """
    notice_file = data_path + 'notice/notice%d' % user_id

    # 判断文件存不存在
    if os.path.exists(notice_file) == False:
        with open(notice_file, 'w', encoding='utf-8') as f:
            pass

    with open(notice_file, 'r', encoding='utf-8') as notice:
        notice_list = notice.readlines()
    time_now = time.time()
    sent = []
    for i in range(len(notice_list)):
        notice_s = notice_list[i]
        notice_l = notice_s.split(maxsplit=2)
        time_set = time.mktime(time.strptime(notice_l[0]+' '+notice_l[1], "%Y-%m-%d %H:%M:%S"))
        if time_set < time_now:
            sent.append(i)
            send_private('提醒：' + notice_l[2][:-1], user_id)
            print(notice_l[2])
    with open(notice_file, 'w', encoding='utf-8') as notice:
        for j in range(len(notice_list)):
            if j not in sent:
                notice.write(notice_list[j])


def show_music(group):
    with open(data_path + 'music', 'r', encoding='utf-8') as music:
        music_list = music.readlines()
    time_now = time.time()
    sent = []
    for i in range(len(music_list)):
        music_s = music_list[i]
        music_l = music_s.split(maxsplit=2)
        time_set = time.mktime(time.strptime(music_l[0] + ' ' + music_l[1], "%Y-%m-%d %H:%M:%S"))
        if time_set < time_now:
            sent.append(i)
            send_group(music_l[2][:-1], group)
            print(music_l[2])
    with open(data_path + 'music', 'w', encoding='utf-8') as music:
        for j in range(len(music_list)):
            if j not in sent:
                music.write(music_list[j])
    time.sleep(1 + random.random())


def life_left():
    now = time.time()

    today = time.strftime('%d', time.localtime(now))
    now_hour = time.strftime('%H', time.localtime(now))

    with open(data_path + 'life_left', 'r', encoding='utf-8') as f:
        records = f.read().split()
    if records[0] == today:  # 是否没有到第二天
        if records[1] == 'yes':  # 今天是否发送过了
            pass
        else:
            if int(now_hour) >= 8:  # 是否到了发送时间
                lived_day = (now - begin) // 86400
                lived_year = round(lived_day / 365.25, 4)
                left_day = (end - now) // 86400
                left_year = round(left_day / 365.25, 4)
                percent = round(lived_day / 29220.0 * 100, 4)

                string = '你已经活了%d天（%.4f年）， 还剩下%d天（%.4f年），人生已过%.4f' % (lived_day, lived_year, left_day, left_year, percent) + '%'
                send_message(string)
                time.sleep(5 + random.random())
                view_account()
                time.sleep(5 + random.random())
                wea = get_weather()
                if wea != 'null':
                    send_group(wea, group_id)
                rec = records[0] + ' yes'
                with open(data_path + 'life_left', 'w', encoding='utf-8') as f:
                    f.write(rec)
                
                print(string)
            else:
                pass
    else:
        rec = today + ' no'
        with open(data_path + 'life_left', 'w', encoding='utf-8') as f:
            f.write(rec)


def video_loader():
    """
    从todo列表获得link，下载并发送视频到群聊。
    """
    todo_path = data_path + 'video_temp/todo'
    if os.path.exists(todo_path):
        with open(todo_path, 'r', encoding='utf-8') as f:
            v_links = f.readlines()
        if len(v_links) > 0:
            v_link = v_links[0]
            if v_link[-1] == '\n':
                v_link = v_link[:-1]
            BiliScratch(v_link)
            if send_video(v_link):
                print('Send video successfully.')
            else:
                print('Send video failed.')
            clean_video_temp()

            with open(todo_path, 'r', encoding='utf-8') as f:
                v_links = f.readlines()
            del v_links[0]
            with open(todo_path, 'w', encoding='utf-8') as f:
                f.writelines(v_links)


if __name__ == '__main__':
    counter = 0
    while True:
        if counter == 0:
            counter = 10
            privates = []
            with open(data_path + 'privates', 'r', encoding='utf-8') as f:
                datas = f.readlines()
                for data in datas:
                    privates.append(int(data))
    
        for user_id in privates:
            send_notice(user_id)
        show_music(group_id)
        life_left()
        video_loader()
        time.sleep(9 + random.random())
        counter -= 1
