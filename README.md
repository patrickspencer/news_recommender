# README

## Requirments

Python version: 3.8

See file `requirements.txt` for python package requirements

## Installation

Install the recommender as a python package
```
python3 setup.py develop
```

## Precomputing values

This command precomputes:
1. Merged articles with articles_users dataframes
2. Top 5 most frequent articles. Each of the 5 articles are from a different category. This is used for the cold start problem
3. tfidf item-item collaborative filtering relationships.
```
sh precompute_relationships.sh 
```

## Notebooks

See `/nokebooks/` folders for some preliminary work on the data.

## Usage

Start the flask server
```
bash start_server.sh
```

See `requests.txt` for sample requests

## About the API request output

The output of the API is an ordered list. Each element of the list is an article. The first element of the list has a higher recommendation score than the second in the list and so on.

### Example Requests

```
The first request is a cold start example. We don't give
a user so we just return the 5 most popular articles spread across different categories. 

Request:

GET http://0.0.0.0:80/api/v1/recommendations HTTP/1.1
content-type: application/json

Output:

[
  {
    "article_id": "db2c8a1cf0ab92c01b887f12aae94ecaa085861e",
    "headline_id": "Trump's last-minute pardons include Bannon, Lil Wayne and scores of others"
  },
  {
    "article_id": "438d69f8171684bc46694a4afe17dda8fde280e0",
    "headline_id": "This town powered America for decades. What do we owe them?"
  },
  {
    "article_id": "38f29c2a6ab4e5230dc34f6dd79b3e4ef62cac17",
    "headline_id": "The face mask that could end the pandemic"
  },
  {
    "article_id": "590310995f40447205e51d908264faedd575ad20",
    "headline_id": "Larry King, legendary talk show host, dies at 87"
  },
  {
    "article_id": "e2292baeb0b99a85afcf4c47c45b8348502efadd",
    "headline_id": "QAnon believers are in disarray after Biden is inaugurated"
  }
]
```

```
The second request queries for a user that already has an
existing history which we use to make enhanced recommendations. You can see these recommendations are more tech and politics related than the cold start recommendations.

Request:

GET http://0.0.0.0:80/api/v1/recommendations?user_id=2bc424123e0a12d29c488bb6e565fe98d0a49b46 HTTP/1.1
content-type: application/json

Output:

[
  {
    "article_id": "d7d1673cedcba0386b0e9748b2ce519434fdb7a0",
    "headline_id": "Biden's desire to stop the border wall could be costly and arduous"
  },
  {
    "article_id": "502474ac9d505fd372ffafab33c3343797fb117d",
    "headline_id": "Pompeo will leave State Department as a Trump loyalist to the very end"
  },
  {
    "article_id": "14e08ac13abdff310f7dba1b365c8096ba88ed0a",
    "headline_id": "Two tech stalwarts fail to impress Wall Street"
  },
  {
    "article_id": "08d9ad8cbe67aeebf499f1418f5e3ad20489ed34",
    "headline_id": "Inside the search for the parents of 545 children separated at the border"
  },
  {
    "article_id": "92d2798566b4f46a4cf4b1bc460e7d036b709780",
    "headline_id": "State Department inspector general becomes the latest watchdog fired by Trump"
  }
]
```

```
The third request is for a return user. You can see these recommendations are more oriented to sports articles.

GET http://0.0.0.0:80/api/v1/recommendations?user_id=dae20ce165bd1f86bd762c246df93efc27e16774 HTTP/1.1
content-type: application/json

Request:
[
  {
    "article_id": "78ccccf7b43d73de4fae43ba8cbe0713fba3b8e5",
    "headline_id": "A four-year timeline of Donald Trump and the Supreme Court"
  },
  {
    "article_id": "6a5fffcced1a38ed6415660cfc5887f64807ad26",
    "headline_id": "Hank Aaron, baseball legend and former home run king, dies at 86"
  },
  {
    "article_id": "5e8b68bb62db821cd0bd774afa7ed49c7163023b",
    "headline_id": "Parents of 628 migrant children separated at border still have not been found, court filing says"
  },
  {
    "article_id": "58bdc869e14309e076407cca6ee9edb2a51d1c4d",
    "headline_id": "Serena Williams' daughter joins her on the tennis court ahead of Australian Open"
  },
  {
    "article_id": "74594805e073774235fde8dfbae86031abcbf0c5",
    "headline_id": "Controversial ad for make-up wipe pulled in China after backlash over alleged victim-blaming"
  }
]
```