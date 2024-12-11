from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

create_mess = []

class AdminBehaviour(HttpUser):
    def create_mess(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        response = self.client.post(
            '/api/messages',
            {
                'roomId': '673fe652d8e700c5b76225af',
                'content': 'Test delete mess ' + salt()
            },
            headers=headers
        )
        create_mess.append(response.json()['data'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(5):
            self.create_mess()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_mess:
            id = create_mess.pop()['_id']
            self.client.delete(
                f'/api/messages/{id}',
                headers=headers
            )
            print(len(create_mess))

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

            self.client.get(
                '/api/messages/room/673fe652d8e700c5b76225af',
                headers=headers
            )

            removed_mess = random.choice(create_mess)
            self.data_id = removed_mess['_id']
            create_mess.remove(removed_mess)

        @task
        def deleteMessWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/messages/{self.data_id}',
                name='/deleted_mess',
                headers=headers
            )
        
        @task
        def createCategory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}
            response = self.client.post(
            '/api/messages',
                {
                    'roomId': '673fe652d8e700c5b76225af',
                    'content': 'Test delete mess ' + salt()
                },
                name='/re-mess',
                headers=headers
            )
            create_mess.append(response.json()['data'])
