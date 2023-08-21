import xml.etree.ElementTree as et
from bot_func.constant import store, data_path, group_id, responds, privates
from bot_func.send import send_group


love_tree = data_path + 'loves.xml'


def create_user(user_id: int, num: int) -> bool:
    """
    创建用户。
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    user = et.Element('user')
    user.attrib['id'] = str(user_id)
    love = et.Element('love')
    love.text = str(num)
    call = et.Element('call')
    call.text = '您'

    user.append(love)
    user.append(call)
    root.append(user)

    tree.write(love_tree, encoding='utf-8', xml_declaration=True)


def add_love(user_id: int, num: int) -> None:
    """
    为QQ号为user_id的用户增加数量为num的erlove值。
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, num)

    else:
        love = root.find('./user[@id="%d"]/love' % user_id)
        love_num = int(love.text)
        love.text = str(love_num + num)
        tree.write(love_tree, encoding='utf-8', xml_declaration=True)

        
def read_love(user_id: int) -> int:
    """
    读取QQ号为user_id的用户的erlove值。
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return 0

    else:
        love = root.find('./user[@id="%d"]/love' % user_id)
        return int(love.text)


def show_store() -> str:
    """
    读取二澪商店。
    """
    store_keys = store.keys()
    s_name = list(store_keys)
    store_list = []
    for item in s_name:
        item += ': ' + str(store[item])
        store_list.append(item)
    store_str = '二澪商店(单位: love)\n' + '\n'.join(store_list)
    return store_str


def buy_item(user_id: int, item_name: str) -> bool:
    """
    用户购买物品。
    """
    if item_name in store:
        tree = et.ElementTree()
        tree.parse(love_tree)
        root = tree.getroot()

        if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
            create_user(user_id, 0)
            return False
        
        else:
            price = store[item_name]
            user = root.find('./user[@id="%d"]' % user_id)
            love = user.find('love')
            user_love = int(love.text)
            if user_love >= price:
                item = user.find('item')
                if item == None:
                    item = et.Element('item')
                    item.text = item_name
                    user.append(item)
                elif item.text == None:
                    item.text = item_name
                else:
                    items = item.text.split()
                    items.append(item_name)
                    item.text = ' '.join(items)
                
                love.text = str(user_love - price)
                tree.write(love_tree, encoding='utf-8', xml_declaration=True)
                return True
            else:
                return False


def rename(user_id: int, name: str) -> bool:
    """
    用户使用改名卡。
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return False

    else:
        user = root.find('./user[@id="%d"]' % user_id)
        item = user.find('item')
        if item == None:
            item = et.Element('item')
            item.text = ''
            user.append(item)
            tree.write(love_tree, encoding='utf-8', xml_declaration=True)
            return False
        else:
            if item.text == None:
                return False
            else:
                items = item.text.split()
                if '改名卡' in items:
                    call = user.find('call')
                    if call == None:
                        call = et.Element('call')
                        call.text = name
                        user.append(call)
                    else:
                        call.text = name
                        items.remove('改名卡')
                        item.text = ' '.join(items)
                    tree.write(love_tree, encoding='utf-8', xml_declaration=True)
                    return True
                else:
                    return False


def read_name(user_id: int) -> str:
    """
    读取用户的称呼。
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return '您'
    
    else:
        user_call = root.find('./user[@id="%d"]/call' % user_id).text
        return user_call


def read_item(user_id: int) -> str:
    """
    读取用户的背包。
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return '（空）'
    
    else:
        user = root.find('./user[@id="%d"]' % user_id)
        item = user.find('item')
        if item == None or item.text == None:
            return '（空）'
        else:
            return item.text


def us_respond(user_id: int) -> int:
    """
    用户使用应和卡。
    @param user_id: 用户QQ号
    @return: int(0 - 2)
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return 0

    else:
        user = root.find('./user[@id="%d"]' % user_id)
        item = user.find('item')
        if item == None:
            item = et.Element('item')
            item.text = ''
            user.append(item)
            tree.write(love_tree, encoding='utf-8', xml_declaration=True)
            return 0
        else:
            if item.text == None:
                return 0
            else:
                items = item.text.split()
                if '应和卡' in items:
                    if user_id in responds:  # 多次使用时返还50点love值
                        items.remove('应和卡')
                        item.text = ' '.join(items)
                        tree.write(love_tree, encoding='utf-8', xml_declaration=True)
                        add_love(user_id, 50)
                        return 2
                    else:
                        with open(data_path + 'responds', 'a', encoding='utf-8') as f:
                            f.write(str(user_id) + '\n')
                        items.remove('应和卡')
                        item.text = ' '.join(items)
                        tree.write(love_tree, encoding='utf-8', xml_declaration=True)
                        return 1
                else:
                    return 0


def set_respond(user_id: int, back_words: str) -> bool:
    """
    用户更改应和用语（默认“好好好”）。
    @param user_id: 用户QQ号
    @param back_words: 应和用语
    @return: bool
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return False

    elif user_id in responds:
        user = root.find('./user[@id="%d"]' % user_id)
        respond_words = user.find('respond_words')
        if respond_words == None:
            respond_words = et.Element('respond_words')
            respond_words.text = back_words
            user.append(respond_words)
            tree.write(love_tree, encoding='utf-8', xml_declaration=True)
            return True
        else:
            respond_words.text = back_words
            tree.write(love_tree, encoding='utf-8', xml_declaration=True)
            return True
    
    return False


def get_respond(user_id: int) -> str:
    """
    获取用户的应和用语（默认“好好好”）。
    @param user_id: 用户QQ号
    @return: str
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    default_words = '好好好'

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return default_words

    else:
        user = root.find('./user[@id="%d"]' % user_id)
        respond_words = user.find('respond_words')
        if respond_words == None:
            return default_words
        else:
            if respond_words.text == '':
                return default_words
            else:
                return respond_words.text


def us_privates(user_id: int) -> int:
    """
    用户使用私聊卡。
    @param user_id: 用户QQ号
    @return: 0：使用失败，1：使用成功，2：重复使用
    """
    tree = et.ElementTree()
    tree.parse(love_tree)
    root = tree.getroot()

    if root.find('./user[@id="%d"]' % user_id) == None:  # 当前用户还没有录入
        create_user(user_id, 0)
        return 0

    else:
        user = root.find('./user[@id="%d"]' % user_id)
        item = user.find('item')
        if item == None:
            item = et.Element('item')
            item.text = ''
            user.append(item)
            tree.write(love_tree, encoding='utf-8', xml_declaration=True)
            return 0
        else:
            if item.text == None:
                return 0
            else:
                items = item.text.split()
                if '私聊卡' in items:
                    if user_id in privates:  # 多次使用时返还100点love值
                        items.remove('私聊卡')
                        item.text = ' '.join(items)
                        tree.write(love_tree, encoding='utf-8', xml_declaration=True)
                        add_love(user_id, 50)
                        return 2
                    else:
                        with open(data_path + 'privates', 'a', encoding='utf-8') as f:
                            f.write(str(user_id) + '\n')
                        items.remove('私聊卡')
                        item.text = ' '.join(items)
                        tree.write(love_tree, encoding='utf-8', xml_declaration=True)
                        with open(data_path + 'notice/notice%d' % user_id, 'w', encoding='utf-8') as f:
                            pass
                        return 1
                else:
                    return 0


def deal_store(info: list, user_id: int) -> None:
    """
    进行商店相关的处理
    """ 
    if info[0] == '商店':
        send_group(show_store(), group_id)
    
    elif info[0] == '购买':
        if len(info) == 1:
            send_group('[CQ:at,qq=%d]%s购买失败' % (user_id, read_name(user_id)), group_id)
        else:
            if buy_item(user_id, info[1]):
                send_group('[CQ:at,qq=%d]%s购买成功' % (user_id, read_name(user_id)), group_id)
            else:
                send_group('[CQ:at,qq=%d]%s购买失败' % (user_id, read_name(user_id)), group_id)
    
    elif info[0] == '背包':
        send_group('%s的背包: %s' % (read_name(user_id), read_item(user_id)), group_id)

    elif info[0] == '改名':
        if len(info) == 1:
            send_group('[CQ:at,qq=%d]%s改名失败' % (user_id, read_name(user_id)), group_id)
        else:
            name = ' '.join(info[1:])
            if rename(user_id, name):
                send_group('[CQ:at,qq=%d]%s改名成功' % (user_id, name), group_id)
            else:
                send_group('[CQ:at,qq=%d]%s改名失败' % (user_id, read_name(user_id)), group_id)

    elif info[0] == '应和卡':
        back = us_respond(user_id)
        if back == 0:
            send_group(read_name(user_id) + '使用应和卡失败', group_id)
        elif back == 1:
            responds.append(user_id)
            send_group(read_name(user_id) + '成功使用应和卡', group_id)
        else:
            send_group(read_name(user_id) + '多次使用应和卡，已返还50点love值', group_id)
    
    elif info[0] == '私聊卡':
        back = us_privates(user_id)
        if back == 0:
            send_group(read_name(user_id) + '使用私聊卡失败', group_id)
        elif back == 1:
            privates.append(user_id)
            send_group(read_name(user_id) + '成功使用私聊卡', group_id)
        else:
            send_group(read_name(user_id) + '多次使用私聊卡，已返还100点love值', group_id)


if __name__ == '__main__' :
    buy_item(1173063330, '私聊卡')
    print(us_privates(1173063330, []))
