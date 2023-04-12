from random import randint
from bot_func.constant import data_path, group_id
from bot_func.send import send_group


def add_food(food_name: str, types: list = None) -> bool:
    """
    添加食物到食物列表。
    """
    with open(data_path + 'food_list', 'r', encoding='utf-8') as f:
        foods_temp = f.readlines()

    foods = []
    for food_temp in foods_temp:
        temp_list = food_temp.split()
        foods.append(temp_list[0])

    if food_name in foods:
        return False
    else:
        if types == None:
            food = food_name + '\n'
        else:
            food = food_name + ' ' + ' '.join(types) + '\n'

        with open(data_path + 'food_list', 'a', encoding='utf-8') as f:
            f.write(food)
        return True


def remove_food(food_name: str) -> bool:
    """
    从食物列表删除食物。
    """
    with open(data_path + 'food_list', 'r', encoding='utf-8') as f:
        foods_temp = f.readlines()

    foods = []
    for food_temp in foods_temp:
        temp_list = food_temp.split()
        foods.append(temp_list[0])

    if food_name not in foods:
        return False
    else:
        foods_temp.remove(foods_temp[foods.index(food_name)])
        with open(data_path + 'food_list', 'w', encoding='utf-8') as f:
            f.writelines(foods_temp)

        return True


def rand_food(types: list = None) -> str:
    """
    从食物列表中随机一种食物并返回。
    """
    with open(data_path + 'food_list', 'r', encoding='utf-8') as f:
        foods_temp = f.readlines()

    foods = []
    if (types == None) or (types == []):
        for food_temp in foods_temp:
            temp_list = food_temp.split()
            foods.append(temp_list[0])
    else:
        for food_temp in foods_temp:
            temp_list = food_temp.split()
            if len(temp_list) > 1:
                is_food_need = True
                for type in types:
                    if type not in temp_list[1:]:
                        is_food_need = False
                if is_food_need:
                    foods.append(temp_list[0])

    if len(foods) == 0:
        return '没有合适的食物'
    else:
        sel = randint(0, len(foods) - 1)
        food = foods[sel]
        return food


def add_food_main(info: list) -> None:
    """
    添加食物。
    """
    if len(info) == 0:
        send_group('格式好像一些问题呢', group_id)
    else:
        if len(info) == 1:
            added = add_food(info[0])
        else:
            added = add_food(info[0], info[1:])
        if added:
            send_group('成功添加 ' + info[0], group_id)
        else:
            send_group('添加失败，已添加过 ' + info[0], group_id)


def del_food_main(info: list) -> None:
    """
    删除食物。
    """
    if len(info) == 1:
        removed = remove_food(info[0])
        if removed:
            send_group('成功删除 ' + info[0], group_id)
        else:
            send_group('删除失败，列表中没有 ' + info[0], group_id)
    else:
        send_group('格式好像一些问题呢', group_id)


if __name__ == '__main__':
    print(add_food('挨打熊', ['a']))
    print(remove_food('挨打熊'))
    print(rand_food(['小吃']))
