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
        def getAllMess(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/messages/room/673fe652d8e700c5b76225af',
                headers=headers
            )
            if response.json()['messages']['isDeleted'] != False:
                self.messages_id = random.choice(response.json()['messages'])['_id']

        @task
        def getMessWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/messages/{self.messages_id}',
                headers=headers,
            )