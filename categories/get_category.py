from locust import HttpUser, task
from common.utils import LOGIN_INFO
import random

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

        response = self.client.get(
            '/api/categories',
            headers=headers
        )

        self.category_id = random.choice(response.json()['categories'])['_id']

    @task
    def getCategoryWithId(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        self.client.get(
            f'/api/categories/{self.category_id}',
            headers=headers
        )