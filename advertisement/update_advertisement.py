from locust import HttpUser, task
from common.utils import LOGIN_INFO
import random

class AdminBehaviour(HttpUser):

    def getAllAdvertisementPackage(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.get(
            '/api/advertisement-packages/',
            headers=headers
        )
        self.advertisementpackage_id = random.choice(list(map(lambda m: m['_id'], response.json()['packages'])))
        print(self.advertisementpackage_id)

    def getAllAdvertisement(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.get(
            '/api/advertisements/',
            headers=headers
        )
        self.advertisement_id= random.choice(list(map(lambda m: m['_id'], response.json()['data'])))
        print(self.advertisement_id)

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        self.getAllAdvertisement()
        self.getAllAdvertisementPackage()

        # headers = {
        #     'Authorization': f'Bearer {self.accessToken}',
        #     'content-type': 'application/json'
        #     }

        # params= {
        #     "videoId": "6768aeddf64923fbea9aecd6",
        #     "packageId": self.advertisementpackage_id
        #     }

        # response = self.client.post(
        #     '/api/advertisements/',
        #     json=params,
        #     headers=headers
        # )
        # print(response.json())

        # self.advertisement_id= response.json()['data']['_id']

    # def on_stop(self):
        # headers = {'Authorization': f'Bearer {self.accessToken}'}

        # response = self.client.delete(
        #     f'/api/advertisements/{self.advertisement_id}',
        #     headers=headers
        # )
        # print(response)

    @task
    def updateAdvertisement(self):
        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'content-type': 'application/json'
        }

        params= {
            "adsId": self.advertisement_id,
            "packageId": self.advertisementpackage_id
        }

        response = self.client.put(
            f'/api/advertisements/extend',
            json=params,
            headers=headers
        )
        # print(response.json())