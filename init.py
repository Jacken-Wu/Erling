import os
import shutil


def new_file(path: str, name: str, content: list = None):
    with open(path + name, 'w', encoding='utf-8') as f:
        if content == None:
            pass
        else:
            f.writelines(content)

data_path = ''
if os.path.exists('./data_path.config'):
    with open('./data_path.config', 'r', encoding='utf-8') as f:
        data_path = f.readline()
    data_path = data_path.replace('\n', '')
else:
    data_path = './data/'
    new_file('./', 'data_path.config', [data_path + '\n'])

is_current = input('是否使用当前目录(%s)(y/n): ' % data_path)
while True:
    if is_current in ['y', 'Y']:
        break
    elif is_current in ['n', 'N']:
        data_path = input('输入数据存储目录：')
        if (data_path[-1] != '/') and (data_path[-1] != '\\'):
            data_path += '/'
        new_file('./', 'data_path.config', [data_path + '\n'])
        break
    else:
        is_current = input('请输入(y/n)进行选择: ')

existed_data_files1 = os.listdir(data_path)
if 'notice' not in existed_data_files1:
    os.mkdir(data_path + 'notice')
if 'trainning' not in existed_data_files1:
    os.mkdir(data_path + 'trainning')
if 'video_temp' not in existed_data_files1:
    os.mkdir(data_path + 'video_temp')

need_files = ['account', 'chat.log', 'food_list', 'music', 'privates', 'responds']
for file in need_files:
    if file not in existed_data_files1:
        new_file(data_path, file)

if 'life_left' not in existed_data_files1:
    new_file(data_path, 'life_left', ['1 no\n'])
if 'loves.xml' not in existed_data_files1:
    new_file(data_path, 'loves.xml', ["<?xml version='1.0' encoding='utf-8'?>\n", '<users>\n', '</users>\n'])
if 'repeat_temp' not in existed_data_files1:
    new_file(data_path, 'repeat_temp', ['Init.'])
if 'songs.xml' not in existed_data_files1:
    new_file(data_path, 'songs.xml', ["<?xml version='1.0' encoding='utf-8'?>\n", '<songs>\n', '</songs>\n'])

existed_data_files2 = os.listdir(data_path + 'trainning/')
if 'conversation' not in existed_data_files2:
    os.mkdir(data_path + 'trainning/conversation')
if 'text' not in existed_data_files2:
    os.mkdir(data_path + 'trainning/text')

if len(os.listdir(data_path + 'trainning/conversation/')) == 0:
    shutil.copyfile('./init_files/conversation_example.yml', data_path + 'trainning/conversation/conversation_example.yml')
if len(os.listdir(data_path + 'trainning/text/')) == 0:
    shutil.copyfile('./init_files/trainning_text_example.txt', data_path + 'trainning/text/trainning_text_example.txt')
if os.path.exists(data_path + 'model_word2vec') == False:
    shutil.copyfile('./init_files/model_word2vec', data_path + 'model_word2vec')
if os.path.exists(data_path + 'constant.config') == False:
    shutil.copyfile('./init_files/constant.config', data_path + 'constant.config')
if os.path.exists(data_path + 'database_conversation.yml') == False:
    shutil.copyfile('./init_files/database_conversation_example.yml', data_path + 'database_conversation.yml')
if os.path.exists(data_path + 'video_temp/todo') == False:
    new_file(data_path + 'video_temp/', 'todo')

print('初始化成功，请查看/更改%sconstant.config中的信息' % data_path)
input('按下Enter键继续')
