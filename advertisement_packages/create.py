from locust import HttpUser, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO
import random

create_advertisement_package_id = []

class AdminBehaviour(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')

        headers = {'Authorization': f'Bearer {accessToken}'}

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

            coin = random.randint(1000, 20000)
            # dateUnit = random.choice(['DAY', 'MONTH', 'YEAR'])
            # numberOfDateUnit = random.randint(1, 30)

            print('isNan', coin == None)
            print('type', type(coin))
            print('is positive', coin > 0)
            print(type(coin) == type(1000))

            response = self.client.post(
                "/api/advertisement-packages/",
                json={
                    "coin": 1000,
                    "dateUnit": "MONTH",
                    "numberOfDateUnit": 30
                },
                headers=headers
            )
            print(response.json())

            create_advertisement_package_id.append(response.json()['packages']['_id'])

            self.clear()