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
        def getAllStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/streams',
                headers=headers
            )

            self.stream_id = random.choice(response.json()['streams'])['_id']

        @task
        def getGiftHistoryWithStreamId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            with self.client.get(
                f'/api/gift-history/streams/{self.stream_id}',
                headers=headers,
                name='/gift-history-stream'
            , catch_response=True) as response:
                if response.status_code == 404:
                    response.success()