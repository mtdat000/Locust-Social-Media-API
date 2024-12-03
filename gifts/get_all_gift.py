from locust import HttpUser, task
from common.utils import LOGIN_INFO

class UserBehavior(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['bao']
        )
        self.accessToken = response.json().get('accessToken')

    @task
    def getAllCategories(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        self.client.get(
            '/api/gifts/',
            headers=headers
        )