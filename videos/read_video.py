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
        def getAllVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/videos/',
                headers=headers
            )

            check_video = random.choice(response.json()['videos'])
            while check_video['enumMode'] != 'public':
                check_video = random.choice(response.json()['videos'])

            self.video_id = check_video

        @task
        def getVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/videos/{self.video_id}',
                headers=headers,
                name='/videos'
            )