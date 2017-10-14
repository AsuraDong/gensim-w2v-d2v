import re
import jieba
import time
import gensim.models.doc2vec as d2v

class SentenceClass(object):
    def __init__(self):
        self.file = None
    def __iter__(self):
        return self
    def __next__(self):
        return self.file.__next__()
    def open_file(self,file):
        self.file = open(file,'r',encoding='utf-8')
    def close_file(self):
        try:
            self.file.close()
        except Exception as e:
            pass

def yield_file(file):
    with open(file,'r',encoding='utf-8') as f:
        for line_no,line in enumerate(f.readlines()):
            print(line)
            yield d2v.TaggedDocument(line.split(' '),tags="%d" % line_no) # 传入的必须是字符串切成的list列表


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
    model_name = '倚天屠龙记_model_d2v.ml'
    # sentences = w2v.LineSentence('倚天屠龙记_cut.txt')
    fout =  open('倚天屠龙记_cut.txt','r',encoding='utf-8')

    sentences = d2v.TaggedLineDocument(fout)
    model = d2v.Doc2Vec(documents=sentences, size=100000, window=5, min_count=5, workers=4)

    # min_count: word frequency of every word
    # size: the numbers of layer
    # workers: threding numbers in building modle, but only works in CPython

    model.save(model_name)
    fout.close()
    print("Finish train and save model")

def train_model_yeild():
    model_name = '倚天屠龙记_model_d2v_yield.ml'

    # 使用样例TaggedDocument
    # fout = open('倚天屠龙记_cut.txt', 'r', encoding='utf-8')
    #
    # lines = []
    # for line in fout.readlines():
    #     lines.append(line)
    # fout.close()
    # res = []
    # sentences = d2v.TaggedDocument(lines[10],tags="1") // 字符串类型
    # res.append(sentences)
    # model = d2v.Doc2Vec(res, size=100, window=5, min_count=5, workers=4)
    # model.save(model_name)

    # 类的使用样例
    # sentences = SentenceClass()
    # file = '倚天屠龙记_cut.txt'
    # sentences.open_file(file)
    # model = d2v.Doc2Vec(sentences, size=100, window=5, min_count=5, workers=4)


    sentences = yield_file('倚天屠龙记_cut.txt')

    model = d2v.Doc2Vec(sentences, size=1000, window=5, min_count=5, workers=4)
    model.save(model_name)

    print("Finish train and save model")

def test():
    model_name = '倚天屠龙记_model_d2v_yield.ml'
    model = d2v.Doc2Vec.load(model_name)
    for i in model.wv.vocab:
        if len(i)>=2:
            print(i)

    # print(model.wv['张三丰'])
    # print(model.wv.vocab)
    # print(model.most_similar(['张无忌'],topn = 5))


if __name__=="__main__":

    start_time = time.time()
    train_model_yeild()
    # train_model()
    # test()

    end_time = time.time()
    print(end_time-start_time,'seconds')
    test()
    # start_time = time.time()
    # train_model()
    # end_time = time.time()
    # print(end_time - start_time, 'seconds')