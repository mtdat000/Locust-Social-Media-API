from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_gift_history_id = []

class UserBehavior(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['bao']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_gift_history_id:
            id = create_gift_history_id.pop()
            self.client.delete(
                f'/api/gift-history/{id}',
                headers=headers
            )
            print(len(create_gift_history_id))

    @task
    class Flow(SequentialTaskSet):
        def getUser(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                f"/api/users/{id}",
                headers=headers
            )

            self.user = response.json()['user']

        def supplyCoin(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                "/api/users/{self.user['_id']}/wallet",
                {
                    'amount': self.gift['valuePerUnit'],
                    'actionCurrencyType': 'ReceiveCoin',
                    'exchangeRate': 0
                },
                headers=headers
            )

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')
            self.userId = response.json().get('userId')
            self.getUser()

        @task
        def getAllStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/streams',
                headers=headers
            )

            self.stream = random.choice(response.json()['streams'])['_id']

        @task
        def getAllGift(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/gifts/',
                headers=headers
            )

            self.gift = random.choice(response.json()['gifts'])['_id']

        @task
        def createGiftHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            if(self.user['wallet']['coin'] < self.gift['valuePerUnit']):
                self.supplyCoin()

            response = self.client.post(
                '/api/gift-history/',
                {
                    'streamId': self.stream['_id'],
                    'gifts': [
                        {
                            'giftId': self.gift['_id'],
                            'quantity': 1
                        }
                    ]
                },
                headers=headers
            )
            create_gift_history_id.append(response.json()['giftHistory']['_id'])