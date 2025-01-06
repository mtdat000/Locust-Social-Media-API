from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

create_advertisement_package = []

class AdminBehaviour(HttpUser):
    def createAdvertisementPackage(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        response = self.client.post(
            '/api/advertisement-packages/',
            {
                "coin": random.randint(1000, 20000),
                "dateUnit": random.choice(["DAY", "MONTH", "YEAR"]),
                "numberOfDateUnit": random.randint(1, 30)
            },
            name='/re-supply',
            headers=headers
        )
        create_advertisement_package.append(response.json()['packages'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(5):
            self.createAdvertisementPackage()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_advertisement_package:
            id = create_advertisement_package.pop()['_id']
            self.client.delete(
                f'/api/advertisement-packages/{id}',
                headers=headers
            )
            print(len(create_advertisement_package))

    @task
    class Flow(SequentialTaskSet):
        def createAdvertisementPackage(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}
            response = self.client.post(
                '/api/advertisement-packages/',
                {
                    "coin": random.randint(1000, 20000),
                    "dateUnit": random.choice(["DAY", "MONTH", "YEAR"]),
                    "numberOfDateUnit": random.randint(1, 30)
                },
                name='/re-supply',
                headers=headers
            )
            create_advertisement_package.append(response.json()['packages'])

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

            removed_advertisement_package = random.choice(create_advertisement_package)
            self.advertisement_package_id = removed_advertisement_package['_id']
            create_advertisement_package.remove(removed_advertisement_package)

        @task
        def deleteAdvertisementPackageWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/advertisement-packages/{self.advertisement_package_id}',
                name='/deleted_packages',
                headers=headers
            )

            self.createAdvertisementPackage()