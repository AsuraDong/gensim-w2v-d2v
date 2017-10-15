import os,re
import jieba
import gensim.models.doc2vec as d2v
import gensim.models.word2vec

USEER_DICT = os.path.join('dict','userdict')

jieba.load_userdict(USEER_DICT)

try :
    from .package.clean_html import cleanHtml
    from .package.cht_or_chs import cht_to_chs
except:
    from package.clean_html import cleanHtml
    from package.cht_or_chs import cht_to_chs

ROOT = os.path.join('..','d2v-data')
MODEL_PATH = os.path.join('model','news_in_d2v.model')


def check(dir=None):
    def _check(func):
        def __check(*args,**kwargs):
            is_raise = (not os.path.isdir(dir)) or (not os.path.exists(dir))
            if not os.path.isdir(dir):
                raise Exception("A non-directionary OR not exists")
            print("Dir path is right")
            return func(*args,**kwargs)
        return __check
    return _check

@check(ROOT)
def yieldDocument(root):
    for nodir in os.listdir(root):
        _,mode = os.path.splitext(nodir)
        if mode!='.txt':
            continue

        filename = os.path.join(root,nodir)
        with open(filename,'r',encoding='utf-8',errors='ignore') as fin:
            news_content = fin.read()
        try:
            clean_news = cht_to_chs(cleanHtml(news_content))
        except Exception as e:
            continue
        else:
            rule = re.compile(r'[a-z0-9 \t\n，。！？：％“”‘’【】（）\(\)\\…,.!?:%"[\]]',re.I)
            clean_news = rule.sub('',clean_news)
            clean_news = list(jieba.cut(clean_news))
        yield d2v.TaggedDocument(clean_news,tags=nodir)

if __name__ == '__main__':
    documents = yieldDocument(ROOT)

    model = d2v.Doc2Vec(documents=documents,size=1000,workers=32,min_count=5)
    model.save(MODEL_PATH)

    print("Train over")
