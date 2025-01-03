from locust import HttpUser, task, SequentialTaskSet
from common.utils import LOGIN_INFO

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

            self.client.get(
                '/api/receipts',
                headers=headers
            )