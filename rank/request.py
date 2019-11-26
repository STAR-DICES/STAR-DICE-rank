import requests
import json


stories_url = 'http://stories:5000'
reactions_url = 'http://reactions:5000'

class Request:
    def __init__(self, get_stories, get_reactions, timeout=1):
        self._get_stories = get_stories
        self._get_reactions = get_reactions
        self._timeout = timeout

    def get_stories(self):
        return self._get_stories(self._timeout)

    def get_reactions(self, author_id):
        return self._get_reactions(author_id, self._timeout)

class TestResponse:
    def __init__(self, status_code, response_data):
        self.status_code = status_code
        self._json = response_data

    def json(self):
        return self._json


# inserisci mio json
all_stories =   {
                    "stories": [
                        {
                            "id": 1,
                            "title": "gita felice",
                            "text": "remare",
                            "rolls_outcome": [
                                "barca",
                                "remo"
                            ],
                            "theme": "lago",
                            "date": "2019-01-01 19:50:12",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 3,
                            "author_name": "mario rossi"
                        },
                        {
                            "id": 2,
                            "title": "campeggio",
                            "text": "che bello",
                            "rolls_outcome": [
                                "albero",
                                "frutta"
                            ],
                            "theme": "montagna",
                            "date": "2019-01-01 19:55:12",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 3,
                            "author_name": "mario rossi"
                        },
                        {
                            "id": 3,
                            "title": "prendere il sole",
                            "text": "onde",
                            "rolls_outcome": [
                                "onde",
                                "sabbia"
                            ],
                            "theme": "mare",
                            "date": "2019-01-01 19:52:12",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 3,
                            "author_name": "mario rossi"
                        },
                        {
                            "id": 4,
                            "title": "il fresco",
                            "text": "castori",
                            "rolls_outcome": [
                                "barca",
                                "remo"
                            ],
                            "theme": "lago",
                            "date": "2019-01-01 19:53:12",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 3,
                            "author_name": "mario rossi"
                        },
                        {
                            "id": 5,
                            "title": "vasche",
                            "text": "tante nuotate",
                            "rolls_outcome": [
                                "doccia",
                                "cloro"
                            ],
                            "theme": "piscina",
                            "date": "2019-01-02 19:50:02",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 4,
                            "author_name": "stefano rossi"
                        },
                        {
                            "id": 6,
                            "title": "svacco",
                            "text": "gianluca vacchi",
                            "rolls_outcome": [
                                "divano",
                                "poltrona"
                            ],
                            "theme": "casa",
                            "date": "2019-01-02 19:56:02",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 5,
                            "author_name": "stefano grossi"
                        },
                        {
                            "id": 7,
                            "title": "caldo",
                            "text": "che macello",
                            "rolls_outcome": [
                                "onde",
                                "sabbia"
                            ],
                            "theme": "mare",
                            "date": "2019-01-02 19:53:02",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 4,
                            "author_name": "stefano trossi"
                        }
                    ]
                }

all_reactions = {
                    "stories_id": [
                        5,
                        7
                    ]
                }

stories_reacted = {
                    "stories": [
                        {
                            "id": 5,
                            "title": "vasche",
                            "text": "tante nuotate",
                            "rolls_outcome": [
                                "doccia",
                                "cloro"
                            ],
                            "theme": "piscina",
                            "date": "2019-01-02 19:50:02",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 4,
                            "author_name": "stefano rossi"
                        },
                        {
                            "id": 7,
                            "title": "caldo",
                            "text": "che macello",
                            "rolls_outcome": [
                                "onde",
                                "sabbia"
                            ],
                            "theme": "mare",
                            "date": "2019-01-02 19:53:02",
                            "likes": 0,
                            "dislikes": 0,
                            "published": 1,
                            "author_id": 4,
                            "author_name": "stefano trossi"
                        }
                    ]
                    }

# all_stories = json.loads(all_stories)
# all_reactions = json.loads(all_reactions)


def test_get_stories(timeout):
    # aggiungi json dei test e fai riportare quelli
    return TestResponse(200, all_stories )

def real_get_stories(timeout):
    return requests.get(stories_url + "/stories", timeout=timeout)

def test_get_reactions(author_id, timeout):
    # aggiungi un json per la risposta delle reactions
    return TestResponse(200, stories_reacted)

def real_get_reactions(author_id, timeout):
    return requests.get(reactions_url + "/get-reacted-stories/" + str(author_id), timeout=timeout)


test_request = Request(test_get_stories, test_get_reactions)
real_request = Request(real_get_stories, real_get_reactions)
