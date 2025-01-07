from locust import HttpUser, task
from common.utils import LOGIN_INFO

class AdminBehaviour(HttpUser):

    create_advertisement = []

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        print(len(self.create_advertisement))

        for id in self.create_advertisement:
            self.client.delete(
                f'/api/advertisements/{id}',
                headers=headers
            )
            # print(id)
    
    @task
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
        print(response.json())
        self.create_advertisement.append(response.json()['data']['_id'])