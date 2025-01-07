from locust import HttpUser, task, SequentialTaskSet
from common.utils import LOGIN_INFO
import random

class UserBehavior(HttpUser):
    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllUsers(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                "/api/users",
                headers=headers
            )

            self.userId = random.choice(response.json()['users'])['_id']

        @task
        def getAllUserReceipts(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/receipts/user/{self.userId}',
                headers=headers
            )