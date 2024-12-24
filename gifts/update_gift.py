from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

create_gift = []

class AdminBehaviour(HttpUser):
    def create_gift(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        response = self.client.post(
            '/api/gifts/',
            {
                'name': 'Locust Test Gift ' + salt(),
                'valuePerUnit': 69
            },
            files={
                'giftCreateImg': ('tester_img.jpg', open('files/tester_img.jpg', 'rb'), 'image/jpeg'),
            },
            headers=headers
        )
        create_gift.append(response.json()['gift'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(10):
            self.create_gift()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_gift:
            id = create_gift.pop()['_id']
            self.client.delete(
                f'/api/gifts/{id}',
                headers=headers
            )
            print(len(create_gift))

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
        def getAllGifts(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                '/api/gifts/',
                headers=headers
            )

            self.gift_id = random.choice(create_gift)['_id']

        @task
        def updateGiftWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f'/api/gifts/{self.gift_id}',
                {
                    'name': 'Locust Test Updated Gift ' + salt(),
                    'valuePerUnit': 69
                },
                files={
                    'giftUpdateImg': ('tester_img.jpg', open('files/tester_img.jpg', 'rb'), 'image/jpeg'),
                },
                name='/updated_gifts',
                headers=headers
            )