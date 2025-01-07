from locust import HttpUser, task
from common.utils import LOGIN_INFO

class AdminBehavior(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

    @task
    def getAllAdvertisement(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        self.client.get(
            '/api/advertisements/',
            headers=headers
        )