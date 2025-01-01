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
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllGiftHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/gift-history/',
                headers=headers
            )

            self.giftHistory_id = random.choice(response.json()['giftHistory'])['_id']

        @task
        def getGiftHistoryWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/gift-history/{self.giftHistory_id}',
                headers=headers,
                name='/gift-history'
            )