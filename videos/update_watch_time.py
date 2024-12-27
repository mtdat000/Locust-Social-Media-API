from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_video = []

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
            self.userId = response.json().get('userId')
          
        @task
        def updateWatchTime(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f'/api/videos/user/watch-time',
                {
                    'userId': self.userId,
                    'watchTime': random.randint(60, 999)
                },
                headers=headers
            )