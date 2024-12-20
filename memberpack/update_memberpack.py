from locust import HttpUser, task
from common.utils import salt, LOGIN_INFO, randomNumber, randomDateUnit

class AdminBehaviour(HttpUser):

    memberpack_id = ""

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
            "name": "Locust Test Memberpack " + salt(),
            "description": "Memberpack descripttion "+ salt(),
            "price": randomNumber(),
            "durationUnit": randomDateUnit(),
            "durationNumber": randomNumber()
            }

        response = self.client.post(
            '/api/member-pack/',
            json=params,
            headers=headers
        )
        print(response.json())

        self.memberpack_id= response.json()['memberPack']['_id']

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        response=self.client.delete(
            f'/api/member-pack/{self.memberpack_id}',
            headers=headers
        )
        print(response)
    
    @task
    def updateMemberpack(self):
        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'content-type': 'application/json'
            }

        params= {
            "name": "Locust Test Memberpack " + salt(),
            "description": "Memberpack descripttion "+ salt(),
            "price": randomNumber(),
            "durationUnit": randomDateUnit(),
            "durationNumber": randomNumber()
            }

        response = self.client.put(
            f'/api/member-pack/{self.memberpack_id}',
            json=params,
            headers=headers
        )
        print(response.json())