from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_gift_history = []

class UserBehavior(HttpUser):
    def getUser(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.get(
            f"/api/users/{self.userId}",
            name='get-user',
            headers=headers
        )

        self.userInfo = response.json()['user']

    def supplyCoin(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        self.client.put(
            f"/api/users/{self.userInfo['_id']}/wallet",
            {
                'amount': self.gift['valuePerUnit'],
                'actionCurrencyType': 'ReceiveCoin',
                'exchangeRate': 0
            },
            name='supply-coin',
            headers=headers
        )

    def getRandomStream(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.get(
            '/api/streams',
            headers=headers
        )

        self.stream = random.choice(response.json()['streams'])

    def getRandomGift(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.get(
            '/api/gifts/',
            headers=headers
        )

        self.gift = random.choice(response.json()['gifts'])

    def createGiftHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            if(self.userInfo['wallet']['coin'] < self.gift['valuePerUnit']):
                self.supplyCoin()

            response = self.client.post(
                '/api/gift-history/',
                json={
                    "streamId": self.stream['_id'],
                    "gifts": [
                        {
                            "giftId": self.gift['_id'],
                            "quantity": 1
                        }
                    ]
                },
                headers=headers,
                name='/re-supply',
            )

            #print(response.json())

            if response.status_code == 201:
                create_gift_history.append(response.json()['giftHistory'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['bao']
        )
        self.accessToken = response.json().get('accessToken')
        self.userId = response.json().get('userId')
        self.getUser()

        for i in range(5): 
            self.getRandomStream()
            self.getRandomGift()
            self.createGiftHistory()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_gift_history:
            id = create_gift_history.pop()['_id']
            self.client.delete(
                f'/api/gift-history/{id}',
                headers=headers
            )
            print(len(create_gift_history))

    @task
    class Flow(SequentialTaskSet):
        def createGiftHistory(self):
            self.getAllStream()
            self.getAllGift()

            headers = {'Authorization': f'Bearer {self.accessToken}'}

            if(self.userInfo['wallet']['coin'] < self.gift['valuePerUnit']):
                self.supplyCoin()

            response = self.client.post(
                '/api/gift-history/',
                json={
                    "streamId": self.stream['_id'],
                    "gifts": [
                        {
                            "giftId": self.gift['_id'],
                            "quantity": 1
                        }
                    ]
                },
                name='/re-supply',
                headers=headers
            )

            if response.status_code == 201:
                create_gift_history.append(response.json()['giftHistory'])

        def getUser(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                f"/api/users/{self.userId}",
                name='get-user',
                headers=headers
            )

            self.userInfo = response.json()['user']

        def supplyCoin(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f"/api/users/{self.userInfo['_id']}/wallet",
                {
                    'amount': self.gift['valuePerUnit'],
                    'actionCurrencyType': 'ReceiveCoin',
                    'exchangeRate': 0
                },
                name='supply-coin',
                headers=headers
            )

        def getAllStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/streams',
                headers=headers
            )

            self.stream = random.choice(response.json()['streams'])

        def getAllGift(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/gifts/',
                headers=headers
            )

            self.gift = random.choice(response.json()['gifts'])

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
        def getAllGiftHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                '/api/gift-history/',
                headers=headers
            )

            removed_gift_history = random.choice(create_gift_history)
            self.gift_history_id = removed_gift_history['_id']
            create_gift_history.remove(removed_gift_history)

        @task
        def deleteGiftHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/gift-history/{self.gift_history_id}',
                headers=headers,
                name='/deleted-gift-history'
            )

            self.createGiftHistory()