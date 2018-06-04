from os.path import join
from global_.embedding import EmbeddingModel
from utils.cache import LMDBClient
from utils import data_utils
from utils import feature_utils
from utils import settings

global_dir = join(settings.DATA_DIR, 'global')


def dump_author_features_lmdb():
    emb_model = EmbeddingModel.load('scopus')
    cnt = 0
    idf = data_utils.load_data(global_dir, 'feature_idf.pkl')
    LMDB_NAME = "author_100.emb.weighted"
    lc = LMDBClient(LMDB_NAME)
    for paper in data_utils.pubs_load_generator():
        if not "title" in paper or not "authors" in paper:
            continue
        if len(paper["authors"]) > 30:
            print(cnt, paper["sid"], len(paper["authors"]))
        if len(paper["authors"]) > 100:
            continue
        if cnt % 1000 == 0:
            print(cnt, paper["sid"], len(paper["authors"]))
        cnt += 1
        for i, author in enumerate(paper.get('authors', [])):
            author_feature = feature_utils.extract_author_features(paper, i)
            print(author_feature)
            lc.set("%s-%s" % (paper["sid"], i), emb_model.project_embedding(author_feature, idf))


if __name__ == '__main__':
    dump_author_features_lmdb()
