from locust import HttpUser, task
from common.utils import LOGIN_INFO
import random

class AdminBehavior(HttpUser):

    memberpack_id = []

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response= self.client.get(
            '/api/member-pack/',
            headers=headers
        )
        self.memberpack_id= list(map(lambda m: m['_id'], response.json()['memberPack']))
        print(self.memberpack_id)

    @task
    def getMemberpack(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        id = random.choice(self.memberpack_id)

        response= self.client.get(
            f'/api/member-pack/{id}',
            headers=headers
        )
        print(response.json())