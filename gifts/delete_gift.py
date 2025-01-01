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

        for i in range(5):
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
        def createGift(self):
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
                name='/re-supply',
                headers=headers
            )
            create_gift.append(response.json()['gift'])

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
                '/api/gifts',
                headers=headers
            )

            # Look up the list of category but only update categories that pre-created
            removed_category = random.choice(create_gift)
            self.category_id = removed_category['_id']
            create_gift.remove(removed_category)

        @task
        def deleteGiftWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/gifts/{self.category_id}',
                name='/deleted_gifts',
                headers=headers
            )

            self.createGift()