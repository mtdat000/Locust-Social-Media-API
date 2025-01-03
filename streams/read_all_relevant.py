from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
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
        def getAllCategory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/categories',
                headers=headers
            )

            self.category_id = random.choice(response.json()['categories'])['_id']
            
        @task
        def getAllRelevantStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                '/api/streams/relevant',
                params={
                    'page': 1,
                    'size': 100,
                    'categoryIds': self.category_id
                },
                headers=headers,
                name='/relevant-videos'
            )