from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_video_id = []

class UserBehavior(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['bao']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_video_id:
            id = create_video_id.pop()
            self.client.delete(
                f'/api/videos/{id}',
                headers=headers,
                name='/cleanup'
            )
            print(len(create_video_id))

    @task
    class Flow(SequentialTaskSet):
        def clear(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            while create_video_id:
                id = create_video_id.pop()
                self.client.delete(
                    f'/api/videos/{id}',
                    headers=headers,
                    name='/cleanup'
                )

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def createVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.post(
                '/api/videos/',
                files={
                    'video': ('tester_video.mp4', open('files/tester_video.mp4', 'rb'), 'video/mp4')
                },
                headers=headers
            )
            create_video_id.append(response.json()['video']['_id'])

            self.clear()