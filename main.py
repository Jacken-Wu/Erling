import json
import socket
from bot_func.notice import *
from bot_func.account import *
from bot_func.send import *
from bot_func.repeat import repeat
from bot_func.constant import *
from bot_func.random_song import add4father_group, add4father_private, add4normal_group, add4normal_private, push_song, order_song
from bot_func.errand import *
from bot_func.what_eat import rand_food, add_food_main, del_food_main
from bot_func.erlove import *
from bot_func.ertrans import *
from bot_func.friend import *
from bot_func.chat import reply_conversation, save_chat, update_conversation, generate_conversation, generate_vec
from bot_func.erhelp import *
from bot_func.say_hi import *
from bot_func.respond import respond_group
from bot_func.biliVideo import add_video_todo, clean_video
from bot_func.weather import get_weather


ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)


def json_to_dic(json_text):
    for i in range(len(json_text)):
        if json_text[i] == '{':
            return json.loads(json_text[i:], strict=False)
    return None


def get_message() -> dict:
    conn, addr = ListenSocket.accept()
    mes = json_to_dic(conn.recv(4096).decode('utf-8', 'ignore'))
    return mes


while True:
    message = get_message()
    print(message)

    if message['post_type'] == 'message' and message['message_type'] == 'private':
        if message['user_id'] == father_id:
            add_love(father_id, 1)
            pri_mess = message['message']

            if pri_mess == '二澪':
                send_message('在')
            elif pri_mess == '提醒查看':
                view_notice(father_id)
            elif pri_mess == '记账查看':
                view_account()
            elif pri_mess == '记账备份':
                backup_account()
            elif pri_mess == '推歌查看':
                view_music()
            elif pri_mess == '生成对话':
                if generate_conversation():
                    send_message('成功生成对话库')
            elif pri_mess == '重加载对话':
                if update_conversation():
                    send_message('成功重新加载对话库')
            elif pri_mess == '生成词向量':
                if generate_vec():
                    send_message('成功生成词向量模型')
            elif pri_mess == 'erlove':
                love = read_love(father_id)
                back = 'love值!%d!' % love
                send_message(back)
            elif pri_mess == '清除视频缓存':
                num = clean_video()
                if num == -1:
                    send_message('清理出现问题，请后台检查')
                else:
                    send_message('已清理%d条视频缓存' % (num // 2))

            elif len(pri_mess) >= 4 and pri_mess[:4] == 'help':
                help_func = pri_mess.split()[1:]
                help_father(help_func)

            if len(pri_mess) >= 6:
                try:
                    if pri_mess[:4] == '提醒添加':
                        add_notice(message['message'][5:], father_id)
                    elif pri_mess[:4] == '提醒删除':
                        del_notice(message['message'][5:], father_id)
                    elif pri_mess[:4] == '记账支出':
                        out_account(message['message'][5:])
                    elif pri_mess[:4] == '记账收入':
                        in_account(message['message'][5:])
                    elif pri_mess[:4] == '记账删除':
                        del_account(message['message'][5:])
                    elif pri_mess[:4] == '推歌添加':
                        add_music(message['message'][5:])
                    elif pri_mess[:4] == '推歌删除':
                        del_music(message['message'][5:])
                    elif pri_mess[:4] == '添加歌曲':
                        info = message['message'][5:].split()
                        add4father_private(info)
                    elif pri_mess[:4] == '通过好友':
                        flag = pri_mess[5:]
                        set_friend(flag)
                except:
                    send_message('语法错误')

        elif message['user_id'] in privates:
            user_id = message['user_id']
            pri_mess = message['message']

            if pri_mess == '二澪':
                send_private('在', user_id)
            elif pri_mess == '提醒查看':
                add_love(user_id, 1)
                view_notice(user_id)
            elif pri_mess == 'erlove':
                love = read_love(user_id)
                back = 'love值!%d!' % love
                send_private(back, user_id)

            elif len(pri_mess) >= 4 and pri_mess[:4] == 'help':
                add_love(user_id, 1)
                help_func = pri_mess.split()[1:]
                help_private(help_func, user_id)

            if len(pri_mess) >= 6:
                try:
                    if pri_mess[:4] == '提醒添加':
                        add_notice(pri_mess[5:], user_id)
                    elif pri_mess[:4] == '提醒删除':
                        del_notice(pri_mess[5:], user_id)
                    elif pri_mess[:4] == '添加歌曲':
                        add_love(user_id, 1)
                        info = pri_mess[5:].split()
                        add4normal_private(info, user_id)
                    add_love(user_id, 1)
                except:
                    send_private('语法错误', user_id)

        else:
            user_id = message['user_id']
            pri_mess = message['message']

            if len(pri_mess) >= 6:
                try:
                    if pri_mess[:4] == '添加歌曲':
                        add_love(user_id, 2)
                        info = pri_mess[5:].split()
                        add4normal_private(info, user_id)
                except:
                    send_private('语法错误', user_id)

    elif message['post_type'] == 'message' and message['message_type'] == 'group' and message['group_id'] == group_id:
        gro_mess = message['message']
        user_id = message['user_id']

        if gro_mess == '二澪':
            add_love(user_id, 1)
            hi_group(user_id)

        elif gro_mess[:2] == 'er':
            if gro_mess[:6] == 'erhelp':
                add_love(user_id, 1)
                erhelp = gro_mess.split()[1:]
                help_group(erhelp, group_id)

            elif gro_mess[:6] == 'errand':
                add_love(user_id, 2)
                errand(gro_mess.split()[1:])

            elif gro_mess[:6] == 'erlove':
                call = read_name(user_id)
                love = read_love(user_id)
                back = '[CQ:at,qq=%d]二澪对%s的love值为%d' % (user_id, call, love)
                send_group(back, group_id)

        elif gro_mess in ['早', '哦哈哟', '早上好','早安']:
            morning_group(user_id)

        elif gro_mess in ['晚安群友', '群友晚安', '晚安', '睡了', '晚安二澪', '二澪晚安']:
            evening_group(user_id)

        elif gro_mess[:3] == '二澪 ':
            add_love(user_id, 2)
            info = gro_mess.split()[1:]
            if len(info) == 0:
                what_group()

            elif info[0] == '推歌':
                infos = info[1:]
                push_song(infos)

            elif info[0] == '点歌':
                song_title = ' '.join(info[1:])
                order_song(song_title)

            elif info[0] == '添加歌曲':
                info = info[1:]
                if user_id == father_id:
                    add4father_group(info, group_id)
                else:
                    add4normal_group(info, user_id, group_id)

            elif info[0] == '添加食物':
                info = info[1:]
                add_food_main(info)

            elif info[0] == '删除食物':
                info = info[1:]
                del_food_main(info)

            elif info[0] == '吃啥':
                types = info[1:]
                send_group(rand_food(types), group_id)

            elif info[0] in ['商店', '购买', '背包', '改名', '应和卡', '私聊卡']:
                deal_store(info, user_id)

            elif info[0] == '天气':
                wea = get_weather()
                send_group(wea, group_id)

            elif info[0] == '应和语':
                if len(info) == 1:
                    send_group('格式好像有问题呢', group_id)
                else:
                    is_set = set_respond(user_id, ' '.join(info[1:]))
                    if is_set:
                        send_group('设置成功啦！', group_id)
                    else:
                        send_group('设置出错啦', group_id)

            else:
                back = auto2en(gro_mess[3:])
                send_group(back, group_id)

        elif (gro_mess[:3] == '二澪，' or gro_mess[:3] == '二澪,') and len(gro_mess) > 3:
            add_love(user_id, 2)
            input_str = gro_mess[3:]
            reply = reply_conversation(input_str)
            send_group(reply, group_id)
            save_chat(input_str, reply)

        elif ('b23.tv' in gro_mess) or ('bilibili.com/video' in gro_mess):
            add_video_todo(gro_mess)

        elif user_id == last_user:
            add_love(user_id, 1)
            reply = reply_conversation(gro_mess)
            send_group(reply, group_id)
            save_chat(gro_mess, reply)

        elif (user_id in responds) and (len(gro_mess) > 0):
            respond_group(user_id, gro_mess)

        else:
            repeat(gro_mess)

        # 下一句是否需要回答的标志
        last_user = 123456789
        if gro_mess == '二澪':
            last_user = user_id

    elif message['post_type'] == 'notice':
            if 'group_id' in message and message['group_id'] == group_id:
                no_type = message['notice_type']

                # 加群欢迎
                if no_type == 'group_increase':
                    new_id = message['user_id']
                    message_send = '[CQ:at,qq=%d]举朵小花欢迎你！' % new_id
                    send_group(message_send, group_id)

                # 戳一戳
                elif no_type == 'notify' and message['sub_type'] == 'poke' and message['target_id'] == self_id:
                    poke_id = message['user_id']
                    message_send = '[CQ:poke,qq=%d]' % poke_id
                    send_group(message_send, group_id)
                    add_love(poke_id, 1)
            
            elif 'sender_id' in message and message['sender_id'] == father_id:
                no_type = message['notice_type']

                # 戳一戳
                if no_type == 'notify' and message['sub_type'] == 'poke' and message['target_id'] == self_id:
                    message_send = '[CQ:poke,qq=%d]' % father_id
                    send_message(message_send)
                    add_love(father_id, 1)

    elif message['post_type'] == 'request' and message['request_type'] == 'friend':
        user_id = message['user_id']
        back = str(user_id) + '好友请求：' +  message['comment'] + '(' + message['flag'] + ')'
        send_message(back)
