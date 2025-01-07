from locust import HttpUser, task
from common.utils import salt, LOGIN_INFO, randomNumber, randomDateUnit

class AdminBehaviour(HttpUser):

    advertisement_id = []

    def createAdvertisement(self):
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
        self.advertisement_id.append(response.json()['data']['_id'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(30):
            self.createAdvertisement()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        while self.advertisement_id:
            id = self.advertisement_id.pop()
            self.client.delete(
                f'/api/advertisements/{id}',
                headers=headers
            )
            print(len(self.advertisement_id))
    
    @task
    def deleteAdvertisement(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        
        if self.advertisement_id:
            id = self.advertisement_id.pop()
            self.client.delete(
                f'/api/advertisements/{id}',
                headers=headers
            )
            print(len(self.advertisement_id))
        else:
            self.environment.runner.quit()