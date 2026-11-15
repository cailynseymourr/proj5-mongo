"""
Tests for the Submit and Display buttons (the /_submit_times and /display routes).
Run inside the web container:
    docker compose exec web python -m unittest test_brevets -v
Note: these tests clear the controls collection.
"""
import sys
import unittest

sys.argv = [sys.argv[0]]  # unittest gets confused by extra args in pytest

import flask_brevets



class BrevetButtonTests(unittest.TestCase):

    def setUp(self):
        flask_brevets.app.testing = True
        self.client = flask_brevets.app.test_client()
        flask_brevets.db.controls.delete_many({})

    def tearDown(self):
        flask_brevets.db.controls.delete_many({})

    def submit(self, items, brevet_dist="200"):
        return self.client.post("/_submit_times", json={
            "brevet_dist": brevet_dist,
            "begin_time": "2017-01-01T00:00",
            "items": items,
        })

    # ---- Submit button ----
    def test_submit_with_no_controls_is_an_error(self):
        response = self.submit([])
        self.assertEqual(response.status_code, 400)
        self.assertIn("at least one", response.get_json()["error"])

    def test_submit_rejects_distance_outside_brevet_range(self):
        response = self.submit(
            [{"km": "500", "open": "x", "close": "y"}], brevet_dist="200")
        self.assertEqual(response.status_code, 400)

    def test_submit_rejects_non_numeric_distance(self):
        response = self.submit([{"km": "abc", "open": "x", "close": "y"}])
        self.assertEqual(response.status_code, 400)

    def test_submit_saves_to_database(self):
        response = self.submit(
            [{"km": "60", "open": "Sun 1/1 1:46", "close": "Sun 1/1 4:00"}])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(flask_brevets.db.controls.count_documents({}), 1)

    # ---- Display button ----
    def test_display_with_empty_database_shows_message(self):
        response = self.client.get("/display")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No control times", response.data)

    def test_display_shows_saved_entries(self):
        self.submit(
            [{"km": "60", "open": "Sun 1/1 1:46", "close": "Sun 1/1 4:00"}])
        response = self.client.get("/display")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sun 1/1 1:46", response.data)


if __name__ == "__main__":
    unittest.main()