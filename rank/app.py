import datetime
import json
import os

from rank.views import blueprints
# from rank.request import real_request, test_request

from flakon import create_app
from swagger_ui import api_doc


def start(test = False):
    app = create_app(blueprints=blueprints)
    if test:
        app.config['TESTING'] = True
      #  app.request = test_request
    # else:
       # app.request = real_request

    api_doc(app, config_path="./rank/rank-specs.yaml", url_prefix="/api", title="API doc")
    return app



if __name__ == '__main__':
    app = start()
    app.run(host='0.0.0.0')