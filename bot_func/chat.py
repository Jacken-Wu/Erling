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
    else:
        answer.append(line[4:])
del origin


def split_sentence(sentence: str) -> list:
    """
    将句子分割为词语。
    """
    sentence = re.sub("[\s+\.\!\/_.$%^*(++\"\'“”《》]+|[+——！，。？、~·@#￥%……&* ( ) ◆☥♥【】（）《》‘’'-'；：‘]+", "", sentence)
    words = jieba.lcut(sentence)
    return words


def generate_vec() -> None:
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


def generate_conversation() -> None:
    """
    使用词向量生成对话数据库。
    """
    with open(data_path + 'database_conversation.yml', 'w', encoding='utf-8') as f:  # 清空
        pass
    model = Word2Vec.load(data_path + 'model_word2vec')
    pathes = os.listdir(data_path + 'trainning/conversation/')
    for path in pathes:
        with open(data_path + 'trainning/conversation/' + path, 'r', encoding='utf-8') as f:
            origin = f.readlines()
        origin = origin[3:]
        with open(data_path + 'database_conversation.yml', 'a', encoding='utf-8') as f:
            flag = False
            for conver in origin:
                if len(conver) > 4:
                    if conver[:4] == '- - ':
                        # 计算句向量
                        words = split_sentence(conver[4:])
                        length = len(words)
                        vec = np.zeros(20)
                        for word in words:
                            try:
                                vec += model.wv.get_vector(word)
                            except KeyError:
                                pass
                        
                        if length != 0:
                            vec /= length
                        
                        if np.linalg.norm(vec) == 0:
                            flag = False
                        else:
                            f.write('- - ' + str(list(vec)) + '\n')
                            flag = True
                    elif conver[:4] == '  - ':
                        if flag == True:
                            f.write('  - ' + conver[4:])


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
        reply_index = similarities.index(max(similarities))
        for times in range(4):
            # 10%的概率丢弃当前回答，选择下一个最高相似度的回答，重复4次得到最终回答
            i = random.randint(0, 9)
            if i == 0:
                similarities[reply_index] = 0
                reply_index = similarities.index(max(similarities))

        reply = answer[reply_index][:-1]

    return reply


def save_chat(word_in: str, word_out: str):
    """
    保存对话日志。
    """
    with open(data_path + 'chat.log', 'a', encoding='utf-8') as f:
        f.write('%s | %s\n' % (word_in, word_out))


if __name__ == '__main__':
    # generate_vec()
    generate_conversation()
    # model = Word2Vec.load(data_path + 'model_word2vec')
    # print('和“超超”相关度最高的词：')
    # print(model.wv.most_similar('超超',topn=5))
    while True:
        in_str = input()
        if in_str == 'exit':
            break
        else:
            print(reply_conversation(in_str))
