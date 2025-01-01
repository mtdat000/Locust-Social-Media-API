from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

broken_stream = dict()

class UserBehavior(HttpUser):
    def on_stop(self):
        stream_error = [dict(t) for t in {tuple(d.items()) for d in broken_stream}]
        for k, v in stream_error.items():
            print(k, v)


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

            response = self.client.get(
                f'/api/streams',
                headers=headers
            )
            
            self.stream_id = random.choice(response.json()['streams'])['_id']

        @task
        def getStream(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            with self.client.get(
                f'/api/streams/{self.stream_id}',
                headers=headers,
                name='/streams',
                catch_response=True
            ) as response:
                if response.status_code == 500:
                    broken_stream[self.stream_id] = str(response.status_code) + ' ' + response.json()['message']