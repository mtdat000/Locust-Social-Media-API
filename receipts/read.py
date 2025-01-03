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
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllReceipts(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/receipts',
                headers=headers
            )

            self.receipt_id = random.choice(response.json()['receipts']['_id'])

        @task
        def getReceipt(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/receipts/{self.receipt_id}',
                headers=headers,
                name='/receipts'
            )