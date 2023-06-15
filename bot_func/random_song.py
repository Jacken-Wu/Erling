import random
import xml.etree.ElementTree as et
from bot_func.constant import data_path, group_id
from bot_func.send import *


def find_all_songs() -> list:
    """
    找到所有歌曲的节点。
    """
    root = et.fromstring(open(data_path + 'songs.xml', 'r', encoding='utf-8').read())
    return root.findall('song')


def filter_songs_tag(songs: list, songs_tag: str) -> list:
    """
    通过type/tag筛选歌曲。
    :param songs: list, 元素为歌曲节点
    """
    return list(filter(lambda node: songs_tag in node.find('tag').text.split(), songs))


def filter_songs_singer(songs: list, singer: str) -> list:
    """
    通过歌手筛选歌曲。
    :param songs: list, 元素为歌曲节点
    """
    return list(filter(lambda node: singer in node.find('singer').text.split(), songs))


def filter_songs_p(songs: list, p: str) -> list:
    """
    通过P主（作曲家）筛选歌曲。
    :param songs: list, 元素为歌曲节点
    """
    return list(filter(lambda node: p in node.find('p').text.split(), songs))


def find_song_title(songs: list, title: str) -> str:
    """
    通过歌名/曲名查找歌曲。
    :param songs: list, 元素为歌曲节点
    """
    songs_find = list(filter(lambda node: node.find('title').text == title, songs))
    if len(songs_find) == 0:
        return 'Not found.'
    else:
        song = songs_find[0]
        title = song.find('title').text
        singer = song.find('singer').text
        p = song.find('p').text
        url = song.find('url').text
        return '【' + p + '】' + title + '【' + singer + '】' + '(' + url + ')'


def random_song(songs: list) -> str:
    """
    从songs列表中随机抽取一首歌/曲子。
    :param songs: list, 元素为歌曲节点
    """
    length = len(songs)
    if length == 0:
        return 'No such songs.'
    else:
        random_num = random.randint(0, length - 1)
        song = songs[random_num]
        title = song.find('title').text
        singer = song.find('singer').text
        p = song.find('p').text
        url = song.find('url').text
        return '【' + p + '】' + title + '【' + singer + '】' + '(' + url + ')'


def add_song(title: str, url: str, song_tag: str, singer: str, p: str) -> bool:
    """
    添加歌曲到songs.xml。
    """
    tree = et.ElementTree()
    tree.parse(data_path + 'songs.xml')
    root = tree.getroot()
    all_songs = root.findall('song/title')

    if len(list(filter(lambda node: node.text == title, all_songs))) != 0:
        return False
    else:
        song = et.Element('song')
        n = et.Element('title')
        u = et.Element('url')
        t = et.Element('tag')
        s = et.Element('singer')
        p_master = et.Element('p')

        n.text = title
        u.text = url
        t.text = song_tag
        s.text = singer
        p_master.text = p

        song.append(n)
        song.append(u)
        song.append(t)
        song.append(s)
        song.append(p_master)

        root.append(song)
        tree.write(data_path + 'songs.xml', encoding='utf-8', xml_declaration=True)

        return True


def add4father_private(info: list) -> None:
    """
    管理者添加歌曲。
    """
    if len(info) >= 5:
        title = ' '.join(info[:-4])
        url = info[-4]
        s_tag = info[-3].replace(',', ' ')
        singer = info[-2].replace(',', ' ')
        p = info[-1].replace(',', ' ')
        back = add_song(title, url, s_tag, singer, p)
        if back:
            send_message('添加完成')
        else:
            send_message('添加失败')
    else:
        send_message('语法错误')


def add4normal_private(info: list, user_id: int) -> None:
    """
    普通用户添加歌曲。
    """
    if len(info) >= 5:
        send_message(str(user_id) + ': 添加歌曲 ' + ' '.join(info))
        send_private('已提交', user_id)
    else:
        send_private('格式好像一些问题呢', user_id)


def add4father_group(info: list, group_id: int) -> None:
    """
    管理者添加歌曲。
    """
    if len(info) >= 5:
        title = ' '.join(info[:-4])
        url = info[-4]
        s_tag = info[-3].replace(',', ' ')
        singer = info[-2].replace(',', ' ')
        p = info[-1].replace(',', ' ')
        back = add_song(title, url, s_tag, singer, p)
        if back:
            send_group('添加完成', group_id)
        else:
            send_group('添加失败', group_id)
    else:
        send_group('语法错误', group_id)


def add4normal_group(info: list, user_id: int, group_id: int) -> None:
    """
    普通用户添加歌曲。
    """
    if len(info) >= 5:
        send_message(str(user_id) + ': 添加歌曲 ' + ' '.join(info))
        send_group('已提交', group_id)
    else:
        send_group('格式好像一些问题呢', group_id)


def push_song(infos: list) -> None:
    """
    群聊推歌。
    """
    all_songs = find_all_songs()
    if len(infos) == 0:
        send_group(random_song(all_songs), group_id)
    else:
        filter_songs = all_songs
        for i in infos:
            info = i.split(':')
            if (len(info) == 1) or (len(info) >= 3):
                send_group('二澪会努力学着去理解……', group_id)
            elif info[0] == 't':
                filter_songs = filter_songs_tag(filter_songs, info[1])
            elif info[0] == 's':
                filter_songs = filter_songs_singer(filter_songs, info[1])
            elif info[0] == 'p':
                filter_songs = filter_songs_p(filter_songs, info[1])
        send_group(random_song(filter_songs), group_id)


def order_song(song_title: str) -> None:
    """
    群聊点歌。
    """
    all_songs = find_all_songs()
    song_find = find_song_title(all_songs, song_title)
    send_group(song_find, group_id)


if __name__ == '__main__':
    a = find_all_songs()
    b = filter_songs_tag(a, 't1')
    c = find_song_title(a, 'test2')
    print(b, c)
