from locust import HttpUser, task, SequentialTaskSet
from common.utils import LOGIN_INFO
import random

created_advertisement_id = []
accessToken = ""

class AdminBehaviour(HttpUser):

    def createAdvertisement(self):
        headers = {
            'Authorization': f'Bearer {accessToken}',
            'content-type': 'application/json'
            }
        
        params= {
            "videoId": "6768aeddf64923fbea9aecd6",
            "packageId": "6715fbd498671ce393dbc4ff"
            }

        response = self.client.post(
            '/api/advertisements/',
            json=params,
            headers=headers
        )
        created_advertisement_id.append(response.json()['data']['_id'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        global accessToken
        accessToken = response.json().get('accessToken')

        for i in range(2):
            self.createAdvertisement()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {accessToken}'}

        while created_advertisement_id:
            id = created_advertisement_id.pop()
            self.client.delete(
                f'/api/advertisements/{id}',
                headers=headers
            )
            print(len(created_advertisement_id))
    
    @task
    class Flow(SequentialTaskSet):
        def createAdvertisement(self):
            headers = {
            'Authorization': f'Bearer {accessToken}',
            'content-type': 'application/json'
            }
        
            params= {
                "videoId": "6768aeddf64923fbea9aecd6",
                "packageId": "6715fbd498671ce393dbc4ff"
                }

            response = self.client.post(
                '/api/advertisements/',
                json=params,
                headers=headers
            )
            created_advertisement_id.append(response.json()['data']['_id'])

        @task
        def getAllAdvertisement(self):
            headers = {'Authorization': f'Bearer {accessToken}'}

            response = self.client.get(
                '/api/advertisements/',
                headers=headers
            )

            self.advertisement_id = random.choice(list(map(lambda m: m['_id'], response.json()['data'])))
            created_advertisement_id.remove(self.advertisement_id)
    
        @task
        def deleteAdvertisement(self):
            headers = {'Authorization': f'Bearer {accessToken}'}
            
            self.client.delete(
                f'/api/advertisements/{self.advertisement_id}',
                headers=headers
            )

            self.createAdvertisement()