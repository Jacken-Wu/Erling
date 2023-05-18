data_path = ''
father_id = 0
self_id = 0
group_id = 0
last_user = 123456789

# 出生死亡日期
begin = 0
end = 0

# 百度翻译的appid和key
appid = ''
key = ''
salt = ''

# 天气网(http://www.weather.com.cn/)对应城市的代码
weather_id = ''

# 二澪商店
store = {}

# 有应和功能权限的用户
responds = []
# 有私聊功能权限的用户
privates = []


with open('./data_path.config', 'r', encoding='utf-8') as f:
    data_path = f.readline()
data_path = data_path.replace('\n', '')

config_list = []
with open(data_path + 'constant.config', 'r', encoding='utf-8') as f:
    config_list = f.readlines()

for config in config_list:
    config = config[:-1]
    if '#' in config:
        index = config.index('#')
        config = config[:index]
    config = config.replace(' ', '')
    config_temp = config.split(':')
    if (len(config_temp) == 2) and (config_temp[0] != '#') and (config_temp[1] != ''):
        if config_temp[0] == 'father_id':
            father_id = int(config_temp[1])
        elif config_temp[0] == 'self_id':
            self_id = int(config_temp[1])
        elif config_temp[0] == 'group_id':
            group_id = int(config_temp[1])
        elif config_temp[0] == 'begin':
            begin = float(config_temp[1])
        elif config_temp[0] == 'end':
            end = float(config_temp[1])
        elif config_temp[0] == 'appid':
            appid = config_temp[1]
        elif config_temp[0] == 'key':
            key = config_temp[1]
        elif config_temp[0] == 'salt':
            salt = config_temp[1]
        elif config_temp[0] == 'weather_id':
            weather_id = config_temp[1]
        else:
            store[config_temp[0]] = int(config_temp[1])


with open(data_path + 'responds', 'r', encoding='utf-8') as f:
    datas = f.readlines()
    for data in datas:
        responds.append(int(data))

with open(data_path + 'privates', 'r', encoding='utf-8') as f:
    datas = f.readlines()
    for data in datas:
        privates.append(int(data))


print('data_path:', data_path)
print('father_id:', father_id)
print('self_id:', self_id)
print('group_id:', group_id)
print('begin:', begin)
print('end:', end)
print('appid:', appid)
if len(key) > 6:
    print('key:', key[:3] + '****' + key[-3:])
else:
    print('key:', key)
print('salt:', salt)
print('weather_id:', weather_id)
print('store:', store)
print('responds:', responds)
print('privates:', privates)
