import json
import unittest
from models import Movies, Actors
from app import create_app
from flask_sqlalchemy import SQLAlchemy


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
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im4ydU5ucW4tR0Vfa2paT3Zzd2Q2byJ9.eyJpc3MiOiJodHRwczovL2ZzbmRoY25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjEzNmM4MTM1YjQ2ODAwMTNhYmI2ZWYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk5NjkwNTIwLCJleHAiOjE1OTk2OTc3MjAsImF6cCI6ImlOM05ETkJGSkxHQWNQWVFSSHhqMUFRdm96a2JZVjIyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.yzFLRJY1cLI5BxNMAYuLbKhEgAs0DaUH-450cz4sDeAMDrol58Vs4o-uqAErNHbfpJTf82jDEyS-rZT-F489l1HnuCbH6CviFEDLuwMJUy8D4QEcwKYvQusszYNLpijBBd-9f7IZ-gH9JB4pTQ3tZtdstKjaHjob-DQku0YiqszrNhZyZy3WSBj8YtE1mK4W2r6EHZaa2KZUXURRqZL932r76j_wia43B4VFLb1GB288owdrF4sGd4eukZMSLF_UB90j4a1h694cyYLJKBYpgZu5ALIJns5VFoHou9cZt2P1y6Y2snW-_Q8Z6W6vHzNRsa7F9FZhJuXQeiLkmu9Afg'
        }

        self.casting_director = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im4ydU5ucW4tR0Vfa2paT3Zzd2Q2byJ9.eyJpc3MiOiJodHRwczovL2ZzbmRoY25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjU2OTVlZmJiOWZmZDAwNjdlZTc3MTgiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk5NjkwNDM5LCJleHAiOjE1OTk2OTc2MzksImF6cCI6ImlOM05ETkJGSkxHQWNQWVFSSHhqMUFRdm96a2JZVjIyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.HT6vb5auDzt-76R9GaUhIK_d5I76jj6CFlU-vgO-luLvRwpJPmx8gU2wkS8U9e4_qk7K6o3LZE4IRDMbVubcHZusMmvGMNeI1A2Tc7lOWc2q1kRcAs2s4Vmrc_igZ09n8LVeNDjgeUYO2fOQZNg-ggieg81hLp7sqcAU6VtFaNxtWklDl9hMWbOXV2qoSC7qfLxfNv7Pqfm8MFufKDZGaogO6xCttsmuhQAJTXDSZ6ZHhOqnKfXzF24nbVZ54SBxFXLsdR_YP6W3jU-vOlAaPquJypwL2KE4cCC4B51Cwf6ufwhYrrFmaKK6YYzYhT9lZ87WWAaN-Cy5jzbVs0cmyQ'
        }

        self.casting_assistant = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im4ydU5ucW4tR0Vfa2paT3Zzd2Q2byJ9.eyJpc3MiOiJodHRwczovL2ZzbmRoY25kLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjU2OWZiYjczY2MyODAwNmQzMTcyZGUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTk5NjkwNjU0LCJleHAiOjE1OTk2OTc4NTQsImF6cCI6ImlOM05ETkJGSkxHQWNQWVFSSHhqMUFRdm96a2JZVjIyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.oGytt5Pd0QjaLNamRy-XmfY9yH2xYgqI18MBlBp1Gfq84txlYyoeeoPqdITeuGhI0M3iIdMbTy0bQLrIp-tNT_TADNANGm_PsC70aY2RSmk9_j3Y71TawwOZRwmnifqFanlFSbUkWERWR_2My5qRtHK64lgwFqIWObtSwpysDEeiMPIqSUsR28z3M5li88cIHyTlPwLQAhn9bpnjTKdJtWmrL-GqpLxL-6ZTMIeqleI7lR5ERdOE3tPHzCWImMS_WgLZVaNS-hTWaL0BOVHq_UH18uB6Zpw3kYfvP_qwWv5zrFz4h6TeGWfebtKwkOAKVgfrHeZoc-b_orfAwrwNCw'
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
        self.assertEqual(res.status_code, 500)

    def test_rbac_fail_wrong_permissions_cd(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.casting_director
        )
        self.assertEqual(res.status_code, 500)

    def test_rbac_fail_wrong_permissions_ca(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.casting_director
        )
        data = json.loads(res.data)
        print(data)

        res = self.client().patch(
            f"/actors/{data['actor']['id']}",
            json=self.updated_actor,
            headers=self.casting_assistant
        )
        self.assertEqual(res.status_code, 500)

    def test_404(self):
        res = self.client().get(
            '/nonexistent',
            headers=self.executive_producer
        )
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
