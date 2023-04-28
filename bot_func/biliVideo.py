import requests
import re
import json
import subprocess
import os
from bot_func.constant import data_path, group_id
from bot_func.send import send_group


video_path = data_path + 'video_temp/'
count = 0


def BiliScratch(url: str):
    """
    输入视频分享地址，下载B站视频。
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'referer': 'https://www.bilibili.com/'
    }

    resp = requests.get(url = url, headers = headers)

    if resp.status_code == 200:
        playinfos = re.findall("<script>window.__playinfo__=(.*?)</script>", resp.text)
        if len(playinfos) > 0:
            playinfo = playinfos[0] #播放信息读取
            pinfo_json = json.loads(playinfo) #转为python的字典格式

            audio_url = pinfo_json['data']['dash']['audio'][0]['baseUrl']
            video_url = pinfo_json['data']['dash']['video'][0]['baseUrl']

            audio_content = requests.get(url = audio_url, headers = headers).content
            video_content = requests.get(url = video_url, headers = headers).content

            with open(f'{video_path}temp.mp3', mode = 'wb') as f:
                f.write(audio_content)
            with open(f'{video_path}temp.mp4', mode = 'wb') as f:
                f.write(video_content)

            cmd = f'ffmpeg -i {video_path}temp.mp3 -i {video_path}temp.mp4 -acodec copy -vcodec copy {video_path}share{count}.mp4 -y'
            print(cmd)
            subprocess.call(cmd, shell = True)

            count += 1

            return True
    else:
        return False


def clean_video_temp():
    """
    清理下载视频过程中的临时文件。
    """
    if os.path.exists(video_path + 'temp.mp3'):
        os.remove(video_path + 'temp.mp3')
    if os.path.exists(video_path + 'temp.mp4'):
        os.remove(video_path + 'temp.mp4')


def send_video():
    """
    发送下载好的视频到群聊。
    """
    if os.path.exists(video_path + 'share' + str(count) + '.mp4'):
        cq_code = f'[CQ:video,file=file://{video_path + video_id}.mp4]'
        send_group(cq_code, group_id)
        return True
    else:
        return False


if __name__ == '__main__':
    video_id = input("请输入AV/BV号: ")
    BiliScratch(video_id)
    # send_video()
    # clean_video_temp()
