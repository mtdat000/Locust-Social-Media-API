from locust import HttpUser, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO
import random

create_member_pack_id = []

class AdminBehaviour(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')

        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_member_pack_id:
            id = create_member_pack_id.pop()
            self.client.delete(
                f'/api/member-pack/{id}',
                headers=headers
            )
            print(len(create_member_pack_id))

    @task
    class Flow(SequentialTaskSet):
        def clear(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            while create_member_pack_id:
                id = create_member_pack_id.pop()
                self.client.delete(
                    f'/api/member-pack/{id}',
                    headers=headers,
                    name='/cleanup'
                )

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def createAdvertisementPackage(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            member_pack_identifier = "Locust Test Member Pack " + salt()

            response = self.client.post(
                "/api/member-pack/",
                json={
                    "name": member_pack_identifier,
                    "description": member_pack_identifier,
                    "price": random.randint(10, 10000),
                    "durationUnit": random.choice(["DAY", "MONTH", "YEAR"]),
                    "durationNumber": random.randint(1, 30)
                },
                headers=headers
            )
            create_member_pack_id.append(response.json()['memberPack']['_id'])

            self.clear()