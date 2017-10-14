import re

import jieba
import gensim.models.word2vec as w2v


def test_sub():
    _str = r"妈妈，没点男子汉气概！到底走不走？”张君宝道：“师父，郭姑娘一片好意……"
    rule = re.compile(r'[，。！？：“”【】\\…,.!?:"[\]]')
    # rule = re.compile(r'[，！]')
    new_str = rule.sub(' ', _str)
    print(new_str)

def in_out_file():
    fin = open('倚天屠龙记_utf8.txt', 'rb')
    fout = open('倚天屠龙记_cut.txt','w')
    rule = re.compile(r'[，。！？：“”【】《》（）、`\\…,.!?:"[\]]')

    for line in fin.readlines():
        newline = rule.sub('',line.decode('utf-8'))
        newline = ' '.join(jieba.cut(newline))
        print(newline,file=fout,end='')

    fin.close()
    fout.close()

def train_model():
    model_name = '倚天屠龙记_model.ml'
    sentences = w2v.LineSentence('倚天屠龙记_cut.txt')
    model = w2v.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)

    # min_count: word frequency of every word
    # size: the numbers of layer
    # workers: threding numbers in building modle, but only works in CPython

    model.save(model_name)
    print("Finish train and save model")

def test():
    model_name = '倚天屠龙记_model.ml'
    model = w2v.Word2Vec.load(model_name)
    print(model.similarity('赵敏','赵敏'))
    print(model.similarity('周芷若','赵敏'))
    print(model.similarity('韦一笑', '赵敏'))
    print(model.similarity('张三丰','赵敏'))

    print()
    for word,weight in model.similar_by_word('张三丰'):
        print(word,weight)

    sentence = "张无忌赵敏韦一笑"
    cut_sentence = ' '.join(jieba.cut(sentence))

    print()
    print('After cutting:',cut_sentence)
    print(model.doesnt_match(cut_sentence.split()))

    print()
    print(model.most_similar(positive=['张三丰', '张无忌'], negative=['灭绝师太'], topn=1))
    print(model.most_similar(['张无忌'],topn = 5))

    print()
    print(model.similarity('张无忌', '张三丰'))
    print(model.similarity('张无忌', '绝艺'))

    print()
    print(len(model.wv.vocab))
    print('张三丰' in model.wv.vocab)
    print(model.wv.vocab)

    print()
    print(model.wv['张三丰'])
    for i in model.wv.vocab:
        print(i)

if __name__=='__main__':
    # train_model()
    test()