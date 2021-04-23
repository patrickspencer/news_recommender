from newsrecommender.src.recommendations_lib import get_recommendations

user_id = '2bc424123e0a12d29c488bb6e565fe98d0a49b46'

recs = get_recommendations(user_id)

print(recs)
print(type(recs))