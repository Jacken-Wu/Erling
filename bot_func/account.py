from bot_func.send import send_message
import time
from bot_func.constant import data_path


def out_account(out: str) -> None:
    """
    记录支出。
    @param out: 格式为“记账名称 数目”
    """
    out_split = out.split()
    if len(out_split) == 2 and float(out_split[1]):
        add_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        with open(data_path + 'account', 'a', encoding='utf-8') as account:
            account.write('out ' + add_time + ': ' + out + '\n')
        send_message('添加完成(' + add_time + ')')
    else:
        send_message('语法错误')


def in_account(ain: str) -> None:
    """
    记录收入。
    @param ain: 格式为“记账名称 数目”
    """
    in_split = ain.split()
    if len(in_split) == 2 and float(in_split[1]):
        add_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        with open(data_path + 'account', 'a', encoding='utf-8') as account:
            account.write('in ' + add_time + ': ' + ain + '\n')
        send_message('添加完成(' + add_time + ')')
    else:
        send_message('语法错误')


def view_account() -> None:
    """
    查看账本，显示最新3条、总的、近一个月的、近一周的账目。
    """
    with open(data_path + 'account', 'r', encoding='utf-8') as account:
        newest = account.readlines()
    sum_acc = 0.0
    week_acc = 0.0
    month_acc = 0.0
    for every_acc in newest:
        acc = every_acc.split()
        if acc[0] == 'out':
            sum_acc -= float(acc[-1])
        elif acc[0] == 'in':
            sum_acc += float(acc[-1])
        acc_time = time.mktime(time.strptime(acc[1][:-1], "%Y-%m-%d"))
        if acc_time >= (time.time() - 604800):
            if acc[0] == 'out':
                week_acc -= float(acc[-1])
            elif acc[0] == 'in':
                week_acc += float(acc[-1])
        if acc_time >= (time.time() - 2592000):
            if acc[0] == 'out':
                month_acc -= float(acc[-1])
            elif acc[0] == 'in':
                month_acc += float(acc[-1])

    if len(newest) > 3:
        newest = newest[-3:]
    account_str = ''.join(newest)
    account_str += 'total: ' + str(round(sum_acc, 2))
    account_str += '\nmonth: ' + str(round(month_acc, 2))
    account_str += '\nweek: ' + str(round(week_acc, 2))
    send_message(account_str)


def del_account(num: str) -> None:
    """
    删除最新的第num条账目。
    """
    with open(data_path + 'account', 'r', encoding='utf-8') as account:
        tmp = account.readlines()
    num = int(num)
    remove = tmp[-num]
    tmp.remove(tmp[-num])
    with open(data_path + 'account', 'w', encoding='utf-8') as account:
        account.writelines(tmp)
    send_message('删除完成(' + remove[:-1] + ')')


def backup_account() -> None:
    """
    备份账本。
    """
    with open(data_path + 'account', 'r', encoding='utf-8') as account:
        backup = account.read()
    backup_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    with open(data_path + 'account' + backup_time, 'w', encoding='utf-8') as account:
        account.write(backup)
    send_message('备份成功')


if __name__ == '__main__':
    view_account()
