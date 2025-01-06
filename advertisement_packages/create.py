from locust import HttpUser, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO
import random

create_advertisement_package_id = []

class AdminBehaviour(HttpUser):
    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        while create_advertisement_package_id:
            id = create_advertisement_package_id.pop()
            self.client.delete(
                f'/api/advertisement-packages/{id}',
                headers=headers
            )
            print(len(create_advertisement_package_id))

    @task
    class Flow(SequentialTaskSet):
        def clear(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            while create_advertisement_package_id:
                id = create_advertisement_package_id.pop()
                self.client.delete(
                    f'/api/advertisement-packages/{id}',
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

            response = self.client.post(
                '/api/advertisement-packages/',
                {
                    "coin": random.randint(1000, 20000),
                    "dateUnit": random.choice(["DAY", "MONTH", "YEAR"]),
                    "numberOfDateUnit": random.randint(1, 30)
                },
                headers=headers
            )
            create_advertisement_package_id.append(response.json()['gift']['_id'])

            self.clear()