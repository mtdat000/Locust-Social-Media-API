from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO
import random

class UserBehavior(HttpUser):
    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllCategories(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/gifts/',
                headers=headers
            )
            self.category_id = random.choice(response.json()['gifts'])['_id']

        @task
        def getCategoryWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/gifts/{self.category_id}',
                headers=headers,
                name='/gifts'
            )