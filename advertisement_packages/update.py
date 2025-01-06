from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

create_advertisement_package = []

class AdminBehaviour(HttpUser):
    def createAdvertisementPackage(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        response = self.client.post(
            '/api/advertisement-packages/',
            json={
                "coin": random.randint(1000, 20000),
                "dateUnit": random.choice(["DAY", "MONTH", "YEAR"]),
                "numberOfDateUnit": random.randint(1, 30)
            },
            headers=headers
        )
        create_advertisement_package.append(response.json()['packages'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(10):
            self.createAdvertisementPackage()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_advertisement_package:
            id = create_advertisement_package.pop()['_id']
            self.client.delete(
                f'/api/advertisement-packages/{id}',
                headers=headers,
            )
            print(len(create_advertisement_package))

    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllAdvertisementPackages(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                '/api/advertisement-packages/',
                headers=headers
            )

            self.advertisement_package_id = random.choice(create_advertisement_package)['_id']

        @task
        def updateAdvertisementPackageWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f'/api/advertisement-packages/{self.advertisement_package_id}',
                json={
                    "coin": random.randint(1000, 20000),
                    "dateUnit": random.choice(["DAY", "MONTH", "YEAR"]),
                    "numberOfDateUnit": random.randint(1, 30)
                },
                name='/updated_advertisement_packages',
                headers=headers
            )