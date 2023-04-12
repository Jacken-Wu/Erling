data_path = ''
father_id = 0
self_id = 0
group_id = 0

# 出生死亡日期
begin = 0
end = 0

# 百度翻译的appid和key
appid = ''
key = ''
salt = ''

store = {}

with open('./data_path', 'r', encoding='utf-8') as f:
    data_path = f.readline()[:-1]

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
        else:
            store[config_temp[0]] = int(config_temp[1])

print(data_path, father_id, self_id, group_id, begin, end, appid, key, salt, store)
