import requests
import re
import json
import subprocess
import os
from bot_func.constant import data_path, group_id
from bot_func.send import send_group


video_path = data_path + 'video_temp/'


def BiliScratch(v_link: str):
    """
    输入视频分享地址b23.tv后面的字符串，或BV号/AV号，下载B站视频。
    """
    url = 'https://b23.tv/' + v_link
    if v_link[:2] in ['BV', 'bv', 'AV', 'av']:
        url = 'https://bilibili.com/video/' + v_link
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'referer': 'https://www.bilibili.com/'
    }

    resp = requests.get(url=url, headers=headers)

    if resp.status_code == 200:
        playinfos = re.findall(
            "<script>window.__playinfo__=(.*?)</script>", resp.text)
        if len(playinfos) > 0:
            playinfo = playinfos[0]  # 播放信息读取
            pinfo_json = json.loads(playinfo)  # 转为python的字典格式

            if 'data' not in pinfo_json:
                print('pinfo_json无data字段，获取视频信息失败')
                send_group('获取视频信息失败', group_id)
                return False
            elif 'dash' not in pinfo_json['data']:
                print('pinfo_json无dash字段，获取视频信息失败')
                send_group('获取视频信息失败', group_id)
                return False
            elif 'audio' not in pinfo_json['data']['dash']:
                print('pinfo_json无audio字段，获取视频信息失败')
                send_group('获取视频信息失败', group_id)
                return False
            elif 'video' not in pinfo_json['data']['dash']:
                print('pinfo_json无video字段，获取视频信息失败')
                send_group('获取视频信息失败', group_id)
                return False
 
            audio_url = pinfo_json['data']['dash']['audio'][0]['baseUrl']
            video_url = pinfo_json['data']['dash']['video'][0]['baseUrl']

            audio_content = requests.get(
                url=audio_url, headers=headers).content
            video_content = requests.get(
                url=video_url, headers=headers).content

            with open(f'{video_path}temp.mp3', mode='wb') as f:
                f.write(audio_content)
            with open(f'{video_path}temp.mp4', mode='wb') as f:
                f.write(video_content)

            cmd = f'ffmpeg -i {video_path}temp.mp3 -i {video_path}temp.mp4 -acodec copy -vcodec copy {video_path}share_{v_link}.mp4 -y'
            print(cmd)
            subprocess.run(cmd, shell=True)

            return True
    else:
        print("Response:", resp.status_code)
        send_group('网络错误', group_id)
        return False


def clean_video_temp():
    """
    清理下载视频过程中的临时文件。
    """
    if os.path.exists(video_path + 'temp.mp3'):
        os.remove(video_path + 'temp.mp3')
    if os.path.exists(video_path + 'temp.mp4'):
        os.remove(video_path + 'temp.mp4')


def clean_video():
    """
    清理下载视频。
    """
    files = os.listdir(video_path)
    length = len(files)
    if length > 1:
        subprocess.run(f'rm {video_path}share_*', shell=True)
    files = os.listdir(video_path)
    if (len(files) == 1) and (files[0] == 'todo'):
        return length - 1
    else:
        return -1


def send_video(v_link):
    """
    发送下载好的视频到群聊。
    """
    if os.path.exists(video_path + 'share_' + v_link + '.mp4'):
        cq_code = f'[CQ:video,file=file://{video_path}share_{v_link}.mp4]'
        is_send = send_group(cq_code, group_id)
        return is_send
    else:
        return False


def link_cmp(gro_mess: str):
    """
    输入群聊的消息，从中得到分享链接。
    """
    gro_mess = gro_mess.replace('\\', '')
    v_links = re.findall('b23.tv/(.*?)\?', gro_mess)
    if v_links == []:
        gro_mess_2 = gro_mess + '?'
        v_links = re.findall('b23.tv/(.*?)\?', gro_mess_2)
    if v_links == []:
        v_links = re.findall('bilibili.com/video/(.*?)\?', gro_mess)
    if v_links == []:
        gro_mess_2 = gro_mess + '?'
        v_links = re.findall('bilibili.com/video/(.*?)\?', gro_mess_2)
    print(v_links)
    v_link = ''
    if len(v_links) > 0:
        v_link = v_links[0]
        # 去掉链接后可能存在的“/”“\”
        while (v_link[-1] == '/') or (v_link[-1] == '\\'):
            v_link = v_link[:-1]
            if v_link == '':
                break
    return v_link


def add_video_todo(gro_mess):
    """
    分析群聊消息，得到分享链接，添加到视频下载列表。
    """
    todo_path = video_path + 'todo'
    v_link = link_cmp(gro_mess)
    if v_link != '':
        with open(todo_path, 'a', encoding='utf-8') as f:
            f.write(v_link + '\n')


if __name__ == '__main__':
    pass
    # v_link = input("请输入地址号: ")
    # BiliScratch(v_link)
    # send_video(v_link)
    # clean_video_temp()
