from locust import HttpUser, task
from common.utils import LOGIN_INFO
import random

class AdminBehavior(HttpUser):

    advertisement_id = []

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response= self.client.get(
            '/api/advertisements/',
            headers=headers
        )
        self.advertisement_id= list(map(lambda m: m['_id'], response.json()['data']))
        print(self.advertisement_id)

    @task
    def getAdvertisement(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        id = random.choice(self.advertisement_id)

        response= self.client.get(
            f'/api/advertisements/{id}',
            headers=headers
        )
        print(response.json())