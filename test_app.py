import os
import json
import unittest
from models import Movies, Actors
from app import create_app
from flask_sqlalchemy import SQLAlchemy

EXECUTIVE_PRODUCER_JWT = os.environ.get('executive_producer_jwt')
CASTING_DIRECTOR_JWT = os.environ.get('casting_director_jwt')
CASTING_ASSISTANT_JWT = os.environ.get('casting_assistant_jwt')


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client

        self.new_movie = {
            "title": "test title",
            "release_date": "1995-09-14"
        }

        self.updated_movie = {
            "title": "updated test title",
            "release_date": "1995-09-14"
        }

        self.new_actor = {
            "name": "Henry Dashwood",
            "age": 24,
            "gender": "male"
        }

        self.updated_actor = {
            "name": "Henry Dashwood",
            "age": 25,
            "gender": "male"
        }

        self.executive_producer = {
            'Authorization': f"Bearer {EXECUTIVE_PRODUCER_JWT}"
        }

        self.casting_director = {
            'Authorization': f"Bearer {CASTING_DIRECTOR_JWT}"
        }

        self.casting_assistant = {
            'Authorization': f"Bearer {CASTING_ASSISTANT_JWT}"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_create_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_get_movies(self):
        res = self.client().get(
            '/movies',
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_update_movie(self):
        res = self.client().patch(
            f"/movies/1",
            json=self.updated_movie,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        res = self.client().delete(
            f"/movies/{data['movie']['id']}",
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_get_actor(self):
        res = self.client().get(
            '/actors',
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_update_actor(self):
        res = self.client().patch(
            f"/actors/1",
            json=self.updated_actor,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        res = self.client().delete(
            f"/actors/{data['actor']['id']}",
            headers=self.executive_producer
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_rbac_no_headers(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_rbac_fail_wrong_permissions_cd(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.casting_director
        )
        self.assertEqual(res.status_code, 401)

    def test_rbac_fail_wrong_permissions_ca(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.casting_director
        )
        data = json.loads(res.data)

        res = self.client().patch(
            f"/actors/{data['actor']['id']}",
            json=self.updated_actor,
            headers=self.casting_assistant
        )
        self.assertEqual(res.status_code, 401)

    def test_404(self):
        res = self.client().get(
            '/nonexistent',
            headers=self.executive_producer
        )
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
