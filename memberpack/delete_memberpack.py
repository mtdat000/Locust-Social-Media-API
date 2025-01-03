from locust import HttpUser, task
from common.utils import salt, LOGIN_INFO, randomNumber, randomDateUnit

class AdminBehaviour(HttpUser):

    memberpack_id = []
    accessToken = ""

    def createMemberpack(self):
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
        self.memberpack_id.append(response.json()['memberPack']['_id'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(40):
            self.createMemberpack()

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        
        headers = {'Authorization': f'Bearer {accessToken}'}

        while self.memberpack_id:
            id = self.memberpack_id.pop()
            self.client.delete(
                f'/api/member-pack/{id}',
                headers=headers
            )
            print(len(self.memberpack_id))
    
    @task
    def deleteMemberpack(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        
        if self.memberpack_id:
            id = self.memberpack_id.pop()
            self.client.delete(
                f'/api/member-pack/{id}',
                headers=headers
            )
            print(len(self.memberpack_id))
        else:
            self.environment.runner.quit()