import re
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from surprise import Reader, Dataset, SVD, model_selection
from settings import SAVED_MODEL_DIR, DATA_MODEL_DIR

article_user_data = DATA_MODEL_DIR + '/article_user.csv'
article_user = pd.read_csv(article_user_data)
articles_data = DATA_MODEL_DIR + '/articles.csv'
articles = pd.read_csv(articles_data)

df = pd.merge(article_user, articles)

all_articles = pd.merge(article_user, articles)

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(articles['headline'].unique())

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

with open(SAVED_MODEL_DIR + '/cosine_sim.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)

g = df.groupby(['user_id', 'article_id'])['article_id'].count()
article_counts = g.rename('rating').to_frame().reset_index()
number_of_visited_articles = df.groupby(['user_id'])['article_id'].count().to_frame().reset_index().rename({'article_id': 'number_of_visited_articles'}, axis=1)

article_counts_merged = pd.merge(number_of_visited_articles, article_counts)
article_counts_merged['normalized_rating'] = article_counts_merged['rating'] / article_counts_merged['number_of_visited_articles']

# add normalized ratings
df = pd.merge(df, article_counts_merged.drop(['rating'], axis=1))

def get_topic(url):
    # a function for getting the category from the url
    pattern = 'http(s)?://(www|money).cnn.com/\d{4}/\d{2}/\d{2}/(?P<topic>[a-z0-9-]+)/'
    result = re.match(pattern, url)
    topic = None
    if result:
        topic = result.group('topic')
    if not result:
        pattern2 = 'https://www.cnn.com/(?P<topic>[a-z]*)/'
        result = re.match(pattern2, url)
        if result:
            topic = result.group('topic')
    if topic:
        return topic
    else:
        return ''

df['category'] = df.apply(lambda r: get_topic(r['url']), axis=1)

# compute top articles in each category
category_groups = df.groupby(['category', 'article_id', 'headline']).size().reset_index().rename({0: 'frequency'}, axis=1)
# n = 5
# # get the top 5 articles
category_groups = category_groups.sort_values('frequency', ascending=False).groupby('category')\
            .head(1).sort_values(['category', 'frequency'], ascending=False)\
            .sort_values('frequency', ascending=False).head(5)

category_groups.to_csv(DATA_MODEL_DIR + '/top_5_articles.csv', index=False)

svd = SVD()
reader = Reader()
data = Dataset.load_from_df(df[['user_id', 'article_id', 'normalized_rating']], reader)
model_selection.cross_validate(svd, data, measures=['RMSE', 'MAE'])

trainset = data.build_full_trainset()
svd.fit(trainset)

with open(SAVED_MODEL_DIR + '/model.pkl', 'wb') as f:
    pickle.dump(svd, f)