import gensim.models.doc2vec as d2v
import numpy as np
import jieba
import os,pickle

MODEL_PATH = os.path.join('model','news_in_d2v.model')
NEG_DICT = os.path.join('dict','negword.plk')
POS_DICT = os.path.join('dict','posword.plk')
TRAIN_DATA = os.path.join('data','trainset')

def loadEmotionDict():
    '''
    加载感情词典
    :return: 感情词列表(为了保证有序，必须是list类型)
    '''
    emotion_set = set()
    neg_fin = open(NEG_DICT,'rb')
    pos_fin = open(POS_DICT,'rb')

    neg_dict = pickle.load(neg_fin)
    pos_dict = pickle.load(pos_fin)

    neg_fin.close();pos_fin.close();

    for word in neg_dict:
        emotion_set.add(word)
    for word in pos_dict:
        emotion_set.add(word)
    return list(emotion_set)


def toVector(news,emotion_word,model):
    '''
    news => 词向量
    :param news: 文本
    :param emotion_word: 感情词列表
    :param model: 训练好的d2v模型
    :return: 词向量（为了之后的合成转化，必须是list类型）
    '''

    res = [0.0]*len(emotion_word)
    for index,word in enumerate(emotion_word):
        if word in news and word in model.wv:
            # print("  at: %d, word: %s" %(index,word))
            res[index] = np.sum(model.wv[word])
    return res



if __name__=="__main__":
    emotion_word = loadEmotionDict()
    modle = d2v.Doc2Vec.load(MODEL_PATH)

    d2v_vector = []
    for nodir in os.listdir(TRAIN_DATA):
        nodir = os.path.join(TRAIN_DATA,nodir)
        with open(nodir,'r',encoding='utf-8') as fout:
            news = fout.read()
        print("Start ",nodir)
        d2v_vector.append(toVector(news=news,emotion_word=emotion_word,model=modle))
        print("  Over")

    d2v_array = np.array(d2v_vector)
    np.save(os.path.join('model','d2v_array'),d2v_array)
