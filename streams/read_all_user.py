from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

class UserBehavior(HttpUser):
    @task
    class Flow(SequentialTaskSet):
        def getRandomUser(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                "/api/users", 
                headers=headers
            )

            return random.choice(response.json()['users'])['_id']

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllUserStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/streams/user/{self.getRandomUser()}',
                headers=headers,
                name='/user-streams'
            )