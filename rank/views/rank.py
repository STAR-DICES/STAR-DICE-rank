import requests, json
from jsonschema import validate, ValidationError
from flask import request, jsonify, abort
from flakon import SwaggerBlueprint

rank = SwaggerBlueprint('rank', 'rank', swagger_spec='./rank/rank-specs.yaml')

stories_url = 'story docker ip goes here'
requests_url = 'story docker ip goes here'

"""
This function is used to return the top 5 most liked stories that the user could be interested in.
Returned stories are the ones that the user did not like/dislike yet and that are written with the same themes
of the last 3 published stories of the user.
"""
@rank.operation('rank')
def _rank(user_id):
    # lastUsedThemes= [story.theme for story in db.session.query(Story).filter(Story.author_id == user_id).distinct()]
    # likedStories= [like.story_id for like in db.session.query(Like).filter(Like.liker_id==user_id)]
    # dislikedStories= [dislike.story_id for dislike in db.session.query(Dislike).filter(Dislike.disliker_id==user_id)]
    # suggestedStories= (db.session.query(Story).filter(Story.author_id != user_id)
    #                                           .filter(Story.published==1)
    #                                           .order_by(Story.likes.desc())
    #                                           .all())
    # suggestedStories = [story for story in suggestedStories if story.id not in likedStories]
    # suggestedStories = [story for story in suggestedStories if story.id not in dislikedStories]
    # suggestedStories = [story for story in suggestedStories if story.theme in lastUsedThemes][:5]
    # return suggestedStories

    # if not general_validator('rank', user_id):
    #     abort(400)
    
    # stories_resp = request.get(stories_url+"/stories") # response 
    # if stories_req.status_code != 200:
    #     abort(404)

    # reactions_resp = request.get(requests_url + "/get-reacted-stories/" + user_id) # response
    # if stories_req.status_code != 200:
    #     abort(404)
    
    all_stories_json = '''
                        {
                        "stories": [
                            {
                                "story_id": 1,
                                "title": "tua mamma",
                                "text": "troione",
                                "rolls_outcome": [
                                    "dildo",
                                    "frusta"
                                ],
                                "theme": "sesso anale",
                                "date": "2019-01-01 19:50:12",
                                "likes": 0,
                                "dislikes": 0,
                                "published": 1,
                                "author_id": 3,
                                "author_name": "mario rossi"
                            },
                            {
                                "story_id": 1,
                                "title": "tua mamma il ritorno",
                                "text": "troione da combattimento",
                                "rolls_outcome": [
                                    "vasellina",
                                    "bocca"
                                ],
                                "theme": "sesso cattivo",
                                "date": "2019-01-02 19:50:02",
                                "likes": 0,
                                "dislikes": 0,
                                "published": 1,
                                "author_id": 4,
                                "author_name": "stefano rossi"
                            }
                        ]
                        }
        '''
    # json.loads(...)
    # json.dumps( ... , indent=x)

    # load the jsons arrived from the other microservices
    # all_stories = json.loads(stories_resp)
    all_stories = json.loads(all_stories_json)
    # liked_stories = json.loads(reactions_resp.json())
    
    # filter my own stories
    my_stories = [ all_stories["stories"][i] for i in range( 0, len(all_stories["stories"]) ) if all_stories["stories"][i]["author_id"] == user_id ]
    # my_stories = [ story for story in all_stories["stories"] if story.author_id == user_id ]
    
    # last three themes used
    # themes_used = [ story.theme for story in my_stories ]
    # used_themes = [ my_stories["stories"][i]["theme"] for i in range( 0, len(my_stories["stories"]) ) ]
    # last_used_themes = [ use]
    # last_used_themes = [ story.theme for story in my_stories["stories"] ][:3]
    
    # suggested_stories = (all_stories - my_stories) - last_used_themes
    # return jsonify( {"stories": my_stories})
    return 1


def general_validator(op_id, request):
    schema = rank.spec['paths']
    for endpoint in schema.keys():
        for method in schema[endpoint].keys():
            if schema[endpoint][method]['operationId'] != op_id:
                continue

            op_schema = schema[endpoint][method]['parameters'][0]
            if 'schema' not in op_schema:
                return True

            definition= op_schema['schema']['$ref'].split("/")[2]
            schema= rank.spec['definitions'][definition]
            try:
                validate(request.get_json(), schema=schema)
            except ValidationError as error:
                return False
            return True