import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
import unittest
from src import database


class TestInsert(unittest.TestCase):
    def setUp(self):
        print("\nRunning Test for adding document to the database")

        self.text = "This is some random document to test data ingestion in database"
        self.user = "Ankita"
        self.expected_result = {"Data Successfully Ingested"}

    def tearDown(self):
        print("TESTING COMPLETED: db_insert\n")

    def test_db_insert(self):
        timer_start = time.time()
        result = db.db_insert(self.text, self.user)
        self.assertEqual(result, self.expected_result)


class TestSearch(unittest.TestCase):
    def setUp(self):
        print("\nRunning Test for text search")
        self.text = "facing issues"
        self.doc_keys = ["score", "text", "username"]

    def tearDown(self):
        print("TESTING COMPLETED: db_search\n")

    def test_db_search(self):
        timer_start = time.time()
        related_documents = db.db_search(self.text)
        timer_stop = time.time()
        self.assertIsInstance(related_documents, list)
        for document in related_documents:
            self.assertTrue(all([key in self.doc_keys for key in document.keys()]))

        print(
            f"Time taken to retreive search results:{(timer_stop - timer_start) : .2f}sec"
        )


if __name__ == "__main__":
    unittest.main()
