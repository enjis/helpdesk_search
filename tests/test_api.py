import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
import unittest
from src.app import app


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.payload = {"text": "finance"}
        self.headers = {}
        self.incorrect_payload = "finance"

    def tearDown(self):
        print("TESTING COMPLETED: search api")

    def test_200(self):
        response = self.client.post("/search", headers=self.headers, json=self.payload)
        self.assertEqual(response.status_code, 200)

    def test_400(self):
        response = self.client.post(
            "/search", headers=self.headers, json=self.incorrect_payload
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
