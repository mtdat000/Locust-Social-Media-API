from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

create_member_pack = []

class UserBehavior(HttpUser):
    def createMemberpack(self):
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
            name='re-suply',
            headers=headers
        )
        create_member_pack.append(response.json()['memberPack'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(5):
            self.createMemberpack()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_member_pack:
            id = create_member_pack.pop()['_id']
            self.client.delete(
                f'/api/member-pack/{id}',
                headers=headers,
            )
            print(len(create_member_pack))
    @task
    class Flow(SequentialTaskSet):
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
                name='re-suply',
                headers=headers
            )
            create_member_pack.append(response.json()['memberPack'])

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllMemberPacks(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/member-pack/',
                headers=headers
            )
            self.member_pack_id = random.choice(response.json()['memberPack'])['_id']

        @task
        def deleteMemberPackWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/member-pack/{self.member_pack_id}',
                headers=headers,
                name='/deleted_member_packs'
            )