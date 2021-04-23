import pandas as pd
import pickle
from newsrecommender.settings import SAVED_MODEL_DIR, DATA_MODEL_DIR

with open(SAVED_MODEL_DIR + '/cosine_sim.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

with open(SAVED_MODEL_DIR + '/model.pkl', 'rb') as f:
    model = pickle.load(f)

article_user_data = DATA_MODEL_DIR + '/article_user.csv'
article_user = pd.read_csv(article_user_data)
articles_data = DATA_MODEL_DIR + '/articles.csv'
articles = pd.read_csv(articles_data)
top_articles_data = DATA_MODEL_DIR + '/top_5_articles.csv'
top_articles = pd.read_csv(top_articles_data)

all_articles = pd.merge(article_user, articles)

indices = pd.Series(articles.index, index=articles['headline'])

def get_recommendations_from_user_id_headline(user_id: str, headline: str):
    idx = indices[headline]
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    article_indices = [i[0] for i in sim_scores]
    
    articles_tmp = articles.iloc[article_indices][['headline', 'article_id']]
    articles_tmp['est'] = articles_tmp.apply(lambda x: model.predict(user_id, x['article_id']).est, axis=1)
    articles_tmp = articles_tmp.sort_values('est', ascending=False)
    return articles_tmp.head(5)


def get_user_history_headlines(user_id: str) -> list:
    msk = all_articles['user_id'] == user_id
    headlines = list(all_articles[msk]['headline'].unique())
    return headlines

def get_user_recommendations(user_id: str) -> pd.DataFrame:
    dfs = []
    for headline in enumerate(get_user_history_headlines(user_id)):
        user_history_headlines = get_user_history_headlines(user_id)
        for headline in user_history_headlines[:5]:
            recs = get_recommendations_from_user_id_headline(user_id, headline)
            dfs.append(recs)
    d = pd.concat(dfs)
    d.sort_values(by='est', ascending=False)
    return d.head(5)

def check_user(user_id: str) -> bool:
    return user_id in set(article_user['user_id'].unique())

def cold_start() -> pd.DataFrame:
    return top_articles

def get_recommendations(user_id: str) -> pd.DataFrame:
    if check_user(user_id):
        return get_user_recommendations(user_id)
    else:
        return cold_start()