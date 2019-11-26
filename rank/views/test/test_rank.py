import unittest
import json

from rank.app import start
from flask_testing import TestCase
 
class TestHelper(TestCase): # pragma: no cover
    def create_app(self):
        self.app = start(test=True)
        self.context = self.app.app_context()
        self.client = self.app.test_client()
        return self.app

    def tearDown(self):
        self.app = None
        self.context = None
        self.client = None

    def test_from_gateway(self):
        reply = self.client.get('/rank/3')  # Known user_id
        self.assertEqual(reply.status_code, 200)
        result = json.loads(reply.data)
        self.assertEqual(result, {
                                    "stories": [
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
                                 })

    def test_user_not_writer(self):
        reply = self.client.get('/rank/1')  # Known user_id
        self.assertEqual(reply.status_code, 200)
        result = json.loads(reply.data)
        self.assertEqual(result, {
                                    "stories": []
                                 })