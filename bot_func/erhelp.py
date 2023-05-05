from bot_func.send import *


def help_father(msg_list: list) -> None:
    """
    管理者的帮助命令。
    """
    if len(msg_list) == 0:
        func_words = 'function:\nhelp\n提醒查看\n提醒添加\n提醒删除\n记账支出\n记账收入\n记账查看\n记账删除\n记账备份\n推歌添加\n推歌查看\n推歌删除\n添加歌曲\nerlove\n通过好友\n生成对话\n重加载对话\n生成词向量\n清除视频缓存'
        send_message(func_words)
    elif len(msg_list) == 1:
        if msg_list[0] == 'help':
            send_message('help function_name')
        elif msg_list[0] == '提醒查看':
            send_message('提醒查看')
        elif msg_list[0] == '提醒添加':
            send_message('提醒添加 time words\ntime可以是纯数字，表示指定分钟后，也可以是时间“%Y-%m-%d %H:%M:%S”')
        elif msg_list[0] == '提醒删除':
            send_message('提醒删除 num')
        elif msg_list[0] == '记账支出':
            send_message('记账支出 内容')
        elif msg_list[0] == '记账收入':
            send_message('记账收入 内容')
        elif msg_list[0] == '记账查看':
            send_message('记账查看')
        elif msg_list[0] == '记账删除':
            send_message('记账删除 num')
        elif msg_list[0] == '记账备份':
            send_message('记账备份')
        elif msg_list[0] == '推歌添加':
            send_message('推歌添加 time 内容\ntime: 年-月-日-时，内容可有空格')
        elif msg_list[0] == '推歌查看':
            send_message('推歌查看')
        elif msg_list[0] == '推歌删除':
            send_message('推歌删除 num')
        elif msg_list[0] == '添加歌曲':
            send_message('添加歌曲 歌名 网址 类型1,类型2... 歌手1,2... P主1,2...')
        elif msg_list[0] == 'erlove':
            send_message('erlove')
        elif msg_list[0] == '通过好友':
            send_message('通过好友 好友申请id')
        elif msg_list[0] == '生成对话':
            send_message('生成对话')
        elif msg_list[0] == '重加载对话':
            send_message('重加载对话')
        elif msg_list[0] == '生成词向量':
            send_message('生成词向量')
        elif msg_list[0] == '清除视频缓存':
            send_message('清除视频缓存')


def help_private(msg_list: list, user_id: int) -> None:
    """
    私聊的帮助命令。
    """
    if len(msg_list) == 0:
        func_words = 'function:\nhelp\n提醒查看\n提醒添加\n提醒删除\nerlove'
        send_private(func_words, user_id)
    elif len(msg_list) == 1:
        if msg_list[0] == 'help':
            send_private('help function_name', user_id)
        elif msg_list[0] == '提醒查看':
            send_private('提醒查看', user_id)
        elif msg_list[0] == '提醒添加':
            send_private('提醒添加 time words\ntime可以是纯数字，表示指定分钟后，也可以是时间“%Y-%m-%d %H:%M:%S”', user_id)
        elif msg_list[0] == '提醒删除':
            send_private('提醒删除 num', user_id)
        elif msg_list[0] == 'erlove':
            send_private('erlove', user_id)


def help_group(msg_list: list, group_id: int) -> None:
    back = 'erhelp XXX'
    if (len(msg_list) == 0) or (len(msg_list) >= 2):
        back = 'erhelp XXX\n推歌/点歌/添加歌曲/errand/添加食物/删除食物/吃啥/erlove/商店/购买/背包/改名/应和卡/ertrans/私聊卡\n或查看https://jacken-wu.github.io/Erhelp/'
    elif msg_list[1] == '推歌':
        back = '二澪 推歌 [t:类型] [s:歌手] [p:P主]'
    elif msg_list[1] == '点歌':
        back = '二澪 点歌 歌名'
    elif msg_list[1] == '添加歌曲':
        back = '二澪 添加歌曲 歌名 网址 tag1,tag2... 歌手1,2... P主1,2...'
    elif msg_list[1] == 'errand':
        back = 'errand XXX1 XXX2 XXX3 ...'
    elif msg_list[1] == '添加食物':
        back = '二澪 添加食物 食物名称 食物标签(可选)'
    elif msg_list[1] == '删除食物':
        back = '二澪 删除食物 食物名称'
    elif msg_list[1] == '吃啥':
        back = '二澪 吃啥 食物标签(可选)'
    elif msg_list[1] == 'erlove':
        back = 'erlove'
    elif msg_list[1] == '商店':
        back = '二澪 商店'
    elif msg_list[1] == '购买':
        back = '二澪 购买 物品名字'
    elif msg_list[1] == '背包':
        back = '二澪 背包（查看已有物品）'
    elif msg_list[1] == '改名':
        back = '二澪 改名 名字（需持有至少一张改名卡）'
    elif msg_list[1] == '应和卡':
        back = '二澪 应和卡（需持有至少一张应和卡）'
    elif msg_list[1] == 'ertrans':
        back = '二澪 任意语句（回复英文翻译）'
    elif msg_list[1] == '私聊卡':
        back = '二澪 私聊卡'
    send_group(back, group_id)
