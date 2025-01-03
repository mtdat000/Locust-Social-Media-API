from locust import HttpUser, TaskSet, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO

class AdminBehaviour(HttpUser):
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
        def getAllStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/streams',
                headers=headers
            )