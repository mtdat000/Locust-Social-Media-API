from locust import HttpUser, TaskSet, task
from common.utils import salt, LOGIN_INFO, randomNumber, randomDateUnit

create_memberpack_id = []

class AdminBehaviour(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        print(len(create_memberpack_id))

        for id in create_memberpack_id:
            self.client.delete(
                f'/api/member-pack/{id}',
                headers=headers
            )
            print(id)
        # while create_memberpack_id:
        #     id = create_memberpack_id.pop()
        #     self.client.delete(
        #         f'/api/member-pack/{id}',
        #         headers=headers
        #     )
        #     print(len(create_memberpack_id))
    
    @task
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
        print(response.json())
        create_memberpack_id.append(response.json()['memberPack']['_id'])