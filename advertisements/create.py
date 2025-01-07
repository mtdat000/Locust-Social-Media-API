from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_advertisement_id = []

class UserBehavior(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_advertisement_id:
            id = create_advertisement_id.pop()
            self.client.delete(
                f'/api/advertisements/{id}',
                headers=headers,
                name='/cleanup'
            )
            print(len(create_advertisement_id))

    @task
    class Flow(SequentialTaskSet):
        def clear(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            while create_advertisement_id:
                id = create_advertisement_id.pop()
                self.client.delete(
                    f'/api/advertisements/{id}',
                    headers=headers,
                    name='/cleanup'
                )

        def getUser(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                f"/api/users/{self.userId}",
                name='/get-user',
                headers=headers
            )

            self.userInfo = response.json()['user']

        def supplyCoin(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f"/api/users/{self.userInfo['_id']}/wallet",
                {
                    'amount': self.advertisement_package['coin'],
                    'actionCurrencyType': 'ReceiveCoin',
                    'exchangeRate': 0
                },
                name='/supply-coin',
                headers=headers
            )

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')
            self.userId = response.json().get('userId')
            self.getUser()

        @task
        def getAllUserVideos(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                f'/api/videos/user/{self.userId}',
                params={
                    'enumMode': 'public'
                },
                headers=headers
            )

            self.video = random.choice(response.json()['videos'])

        @task
        def getAllAdvertisementPackages(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/advertisement-packages/',
                headers=headers
            )

            self.advertisement_package = random.choice(response.json()['packages'])

        @task
        def createAdvertisement(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            if(self.userInfo['wallet']['coin'] < self.advertisement_package['coin']):
                self.supplyCoin()

            print('User Coin:',self.userInfo['wallet']['coin'], 'Package Value:',self.advertisement_package['coin'])

            response = self.client.post(
                '/api/advertisements/',
                json={
                    "videoId": self.video['_id'],
                    "packageId": self.advertisement_package['_id']
                },
                headers=headers
            )

            print(self.video['_id'])
            print(self.advertisement_package['_id'])
            print(response.json())

            if response.status_code == 201:
                create_advertisement_id.append(response.json()['data']['_id'])

            self.clear()