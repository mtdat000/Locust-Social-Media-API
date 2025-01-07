from locust import HttpUser, task
from common.utils import LOGIN_INFO

class AdminBehaviour(HttpUser):

    advertisement_id = ""

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        headers = {
            'Authorization': f'Bearer {self.accessToken}',
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
        print(response.json())

        self.advertisement_id= response.json()['data']['_id']

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        response=self.client.delete(
            f'/api/advertisements/{self.advertisement_id}',
            headers=headers
        )
        # print(response)
    
    @task
    def updateAdvertisement(self):
        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'content-type': 'application/json'
            }

        params= {
            "adsId": self.advertisement_id,
            "packageId": "6715fbd498671ce393dbc4ff"
            }

        response = self.client.put(
            f'/api/advertisements/extend',
            json=params,
            headers=headers
        )
        # print(response.json())