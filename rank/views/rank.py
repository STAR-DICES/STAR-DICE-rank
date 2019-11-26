import requests, json
from jsonschema import validate, ValidationError
from flask import request, jsonify, abort
from flakon import SwaggerBlueprint

rank = SwaggerBlueprint('rank', 'rank', swagger_spec='./rank/rank-specs.yaml')

stories_url = 'http://stories:5000'
reactions_url = 'http://reactions:5000'

"""
This function is used to return the top 5 most liked stories that the user could be interested in.
Returned stories are the ones that the user did not like/dislike yet and that are written with the same themes
of the last 3 published stories of the user.
"""
@rank.operation('rank')
def _rank(user_id):

    user_id = int(user_id)

    if not general_validator('rank', user_id):
        abort(400)
    
    stories_resp = request.get(stories_url+"/stories") # response 
    if stories_resp.status_code != 200:
        abort(404)

    reactions_resp = request.get(request_url + "/get-reacted-stories/" + user_id) # response
    if reactions_resp.status_code != 200:
        abort(404)
    
    # load the jsons arrived from the other microservices
    # 
    all_stories = json.loads(stories_resp.json())
    liked_stories = json.loads(reactions_resp.json())

    # my own stories
    # 
    my_stories = [ story for story in all_stories["stories"] if story["author_id"] == user_id ]

    # last three themes I used
    # 
    sorted_theme_dates = sorted( [ (story["theme"], story["date"]) for story in my_stories], key= lambda x:x[1] )
    takelasts = 3
    last_themes = [ tuple[0] for tuple in sorted_theme_dates ][:takelasts]
    dist_last_themes = list( set( last_themes ) )

    # stories of other writers
    # 
    drop_own = [ story for story in all_stories["stories"] if story["author_id"] != user_id ]

    # stories with my last used themes
    # 
    select_themes = [ story for story in drop_own if story["theme"] in dist_last_themes ]

    # stories without my interactions (final drop)
    # 
    suggesteds = [ story for story in select_themes if story["story_id"] not in liked_stories ]

    return jsonify( {"stories": suggesteds } )


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