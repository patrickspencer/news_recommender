import flask
from typing import List
from flask import jsonify, request


from newsrecommender.src.recommendations_lib import get_recommendations

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def make_user_output(user_id: str) -> List:
    output = []
    recs = get_recommendations(user_id)
    for i, rec in recs.iterrows():
        d = {}
        d['headline_id'] = rec['headline']
        d['article_id'] = rec['article_id']
        #d['url'] = rec['url']
        output.append(d)
    return output

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/recommendations', methods=['GET'])
def api_recs():
    user_id = request.args.get('user_id')
    return jsonify(make_user_output(user_id))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)