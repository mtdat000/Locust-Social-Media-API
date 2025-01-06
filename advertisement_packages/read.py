from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO
import random

class UserBehavior(HttpUser):
    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllAdvertisementPackages(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/advertisement-packages/',
                headers=headers
            )
            self.advertisement_package_id = random.choice(response.json()['packages'])['_id']

        @task
        def getAdvertisementPackageWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/advertisement-packages/{self.advertisement_package_id}',
                headers=headers,
                name='/advertisement_packages'
            )