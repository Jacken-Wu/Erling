from bot_func.constant import data_path
from gensim.models import Word2Vec
import jieba
import re
import os
import numpy as np
import random


# 读取对话数据库
with open(data_path + 'database_conversation.yml', 'r', encoding='utf-8') as f:
    origin = f.readlines()
asking = []
answer = []
for line in origin:
    if line[:4] == '- - ':
        asking.append(eval(line[4:]))
    elif line[:4] == '  - ':
        answer.append(line[4:])
del origin


def update_conversation() -> bool:
    """
    更新对话库。
    """
    global asking
    global answer

    with open(data_path + 'database_conversation.yml', 'r', encoding='utf-8') as f:
        origin = f.readlines()
    asking = []
    answer = []
    for line in origin:
        if line[:4] == '- - ':
            asking.append(eval(line[4:]))
        elif line[:4] == '  - ':
            answer.append(line[4:])
    del origin

    return True


def split_sentence(sentence: str) -> list:
    """
    将句子分割为词语。
    """
    sentence = re.sub("[\s+\.\!\/_.$%^*(++\"\'“”《》]+|[+——！，。？、~·@#￥%……&* ( ) ◆☥♥【】（）《》‘’'-'；：‘]+", "", sentence)
    words = jieba.lcut(sentence)
    return words


def generate_vec() -> bool:
    """
    生成并保存词向量模型。生成的模型保存在用户自定的data_path下。
    """
    pathes = os.listdir(data_path + 'trainning/text/')
    lines = []
    for path in pathes:
        with open(data_path + 'trainning/text/' + path, 'r', encoding='utf-8') as f:
            text = f.readlines()
        for sentence in text:
            lines.append(split_sentence(sentence))
    model = Word2Vec(lines, vector_size = 20, window=3, min_count=3, epochs=7,negative=10)
    model.save(data_path + 'model_word2vec')
    return True


def generate_conversation() -> bool:
    """
    使用词向量生成对话数据库。
    """
    with open(data_path + 'database_conversation.yml', 'w', encoding='utf-8') as f:  # 清空
        pass
    model = Word2Vec.load(data_path + 'model_word2vec')
    pathes = os.listdir(data_path + 'trainning/conversation/')
    chat_q = []
    chat_a = []
    for path in pathes:
        with open(data_path + 'trainning/conversation/' + path, 'r', encoding='utf-8') as f:
            origin = f.readlines()
        origin = origin[3:]
        for conver in origin:
            if len(conver) > 4:
                if conver[:4] == '- - ':
                    chat_q.append(conver[4:])
                elif conver[:4] == '  - ':
                    chat_a.append(conver[4:])

    chat_vec_temp = []
    chat_answer_tamp = []
    with open(data_path + 'database_conversation.yml', 'a', encoding='utf-8') as f:
        for i in range(len(chat_q)):
            # 计算句向量
            words = split_sentence(chat_q[i])
            length = len(words)
            vec = np.zeros(20)
            for word in words:
                try:
                    vec += model.wv.get_vector(word)
                except KeyError:
                    pass

            if length != 0:
                vec /= length

            vec_string = str(list(vec))
            if (np.linalg.norm(vec) != 0) and (vec_string not in chat_vec_temp) and (chat_a[i] not in chat_answer_tamp):  # 模不为0且Q和A都未重复
                chat_vec_temp.append(vec_string)
                chat_answer_tamp.append(chat_a[i])
                f.write('- - ' + vec_string + '\n')
                f.write('  - ' + chat_a[i])

    return True


def compare(vec1: list, vec2: list) -> float:
    """
    使用夹角余弦值比较两个向量的相似程度，输入两个向量，输出相似度（0~1之间）。
    """
    num = np.dot(vec1, vec2)
    conum = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if conum == 0:
        return 0
    else:
        cos_value = num / conum
        return 0.5 * cos_value + 0.5


def reply_conversation(input_str: str) -> str:
    """
    对输入语句进行答复。
    @param input_str: 输入语句
    """
    model = Word2Vec.load(data_path + '/model_word2vec')
    words = split_sentence(input_str)
    length = len(words)
    input_vec = np.zeros(20)
    for word in words:
        try:
            input_vec += model.wv.get_vector(word)
        except KeyError:
            pass
    if length != 0:
        input_vec /= length

    if np.linalg.norm(input_vec) == 0:
        reply = '这个话题二澪还听不懂呢'
    else:
        similarities = []
        for vec in asking:
            similarities.append(compare(input_vec, vec))

        # 在权重相同的所有回答中随机选择一个
        max_sim = max(similarities)
        reply_indexs = []
        while max(similarities) == max_sim:
            reply_indexs.append(similarities.index(max(similarities)))
            similarities[reply_indexs[-1]] = 0
        reply_index = reply_indexs[random.randint(0, len(reply_indexs) - 1)]

        # 7%的概率丢弃当前回答，选择下一个最高相似度的回答，重复4次得到最终回答
        for times in range(4):
            i = random.randint(0, 99)
            if i < 7:
                reply_index = similarities.index(max(similarities))
                similarities[reply_index] = 0

        reply = answer[reply_index][:-1]

    return reply


def save_chat(word_in: str, word_out: str):
    """
    保存对话日志。
    """
    with open(data_path + 'chat.log', 'a', encoding='utf-8') as f:
        f.write('%s | %s\n' % (word_in, word_out))


def learn_chat(sentence: str, user_id: int):
    """
    将群聊中的对话保存到对话文件。
    @param sentence: str
    @param user_id: int
    @return: int (0：开启新对话，1：清空，2：对话未结束，3：写入对话并开启下一段对话，4：写入对话但清空)
    """
    # 去掉CQ码、换行和空格
    if ('[' in sentence) and (']' in sentence):
        sentence = re.sub(u"\\[.*?]", "", sentence)
    sentence = sentence.replace('\n', '')
    sentence = sentence.replace(' ', '')

    with open(data_path + 'group_chat_temp', 'r', encoding='utf-8') as f:
        chat_temp = f.readlines()
    if chat_temp == []:
        if sentence == '':
            return 1
        with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
            f.write('%d|%s\n' % (user_id, sentence))
        return 0

    chat_temp_last = chat_temp[0].split('|')
    user_last = chat_temp_last[0]
    sentence_last = chat_temp_last[1].replace('\n', '')
    if len(chat_temp) == 1:
        if user_id == int(user_last):
            if sentence == '':
                return 2
            sentence = sentence_last + '，' + sentence
            if len(sentence) > 30:  # 语句太长，清空
                with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
                    pass
                return 1
            with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
                f.write('%d|%s\n' % (user_id, sentence))
            return 2

        if (sentence == '') or (len(sentence) > 30):  # 语句为空或太长，清空
            with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
                pass
            return 1
        with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
            f.write('%s|%s\n%d|%s\n' % (user_last, sentence_last, user_id, sentence))
        return 2

    chat_temp_current = chat_temp[1].split('|')
    user_current = chat_temp_current[0]
    sentence_current = chat_temp_current[1].replace('\n', '')
    if user_id == int(user_current):
        if sentence == '':
            return 2
        sentence = sentence_current + '，' + sentence
        if len(sentence) > 30:  # 语句太长，清空
            with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
                pass
            return 1
        with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
            f.write('%s|%s\n%d|%s\n' % (user_last, sentence_last, user_id, sentence))
        return 2
    
    # 对话结束，将对话写入语料库
    with open(data_path + 'trainning/conversation/group_learn.yml', 'a', encoding='utf-8') as f:
        f.write('- - ' + sentence_last + '\n')
        f.write('  - ' + sentence_current + '\n')
    print('已记录一对语句')

    if (sentence == '') or (len(sentence) > 30):  # 语句为空或太长，清空
        with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
            pass
        return 4
    # 更新sentence次序
    with open(data_path + 'group_chat_temp', 'w', encoding='utf-8') as f:
        f.write('%s|%s\n%d|%s\n' % (user_current, sentence_current, user_id, sentence))
    return 3


if __name__ == '__main__':
    # generate_vec()
    generate_conversation()
    update_conversation()
    # model = Word2Vec.load(data_path + 'model_word2vec')
    # print('和“超超”相关度最高的词：')
    # print(model.wv.most_similar('超超',topn=5))
    while True:
        in_str = input()
        if in_str == 'exit':
            break
        else:
            print(reply_conversation(in_str))
