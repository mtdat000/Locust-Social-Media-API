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
        def getAllStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/streams',
                headers=headers
            )

            self.video_id = random.choice(response.json()['streams'])['_id']

        @task
        def toggleStreamLike(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.post(
                f'/api/streams/{self.video_id}/like',
                headers=headers,
                name="/like-stream"
            )