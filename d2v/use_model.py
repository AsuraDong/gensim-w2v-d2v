import gensim.models.doc2vec as d2v
import os

MODEL_PATH = os.path.join('model','news_in_d2v.model')

if __name__=="__main__":
    model = d2v.Doc2Vec.load(MODEL_PATH)
    print(len(model.wv.vocab))
    for key in model.wv.vocab:
        if len(key)>1:
            print(key)