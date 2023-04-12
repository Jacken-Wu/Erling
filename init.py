import os
import shutil


def new_file(path: str, name: str, content: list = None):
    with open(path + name, 'w', encoding='utf-8') as f:
        if content == None:
            pass
        else:
            f.writelines(content)


data_path = input('输入存储data数据的目录（最好新建一个空文件夹）：')
if (data_path[-1] != '/') or (data_path[-1] != '\\'):
    data_path += '/'
with open('./data_path', 'w', encoding='utf-8') as f:
    f.write(data_path + '\n')

existed_data_files1 = os.listdir(data_path)
if 'notice' not in existed_data_files1:
    os.mkdir(data_path + 'notice')
if 'trainning' not in existed_data_files1:
    os.mkdir(data_path + 'trainning')

existed_data_files2 = os.listdir(data_path + 'trainning/')
if 'conversation' not in existed_data_files2:
    os.mkdir(data_path + 'trainning/conversation')
if 'text' not in existed_data_files2:
    os.mkdir(data_path + 'trainning/text')

need_files = ['account', 'chat.log', 'food_list', 'music', 'privates', 'responds', 'database_conversation.yml']
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

if os.path.exists(data_path + 'trainning/conversation/conversation_example.yml') == False:
    shutil.copyfile('./init_files/conversation_example.yml', data_path + 'trainning/conversation/conversation_example.yml')
if os.path.exists(data_path + 'trainning/text/trainning_text_example.txt') == False:
    shutil.copyfile('./init_files/trainning_text_example.txt', data_path + 'trainning/text/trainning_text_example.txt')
if os.path.exists(data_path + 'model_word2vec') == False:
    shutil.copyfile('./init_files/model_word2vec', data_path + 'model_word2vec')
if os.path.exists(data_path + 'constant.config') == False:
    shutil.copyfile('./init_files/constant.config', data_path + 'constant.config')
