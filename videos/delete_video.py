from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_video = []

class UserBehavior(HttpUser):
    def createVideo(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.post(
            '/api/videos/',
            files={
                'video': ('tester_video.mp4', open('files/tester_video.mp4', 'rb'), 'video/mp4')
            },
            headers=headers
        )
        create_video.append(response.json()['video'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['bao']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(2):
            self.createVideo()

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['bao']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_video:
            id = create_video.pop()['_id']
            self.client.delete(
                f'/api/videos/{id}',
                headers=headers,
                name='/cleanup'
            )
            print(len(create_video))
        
    @task
    class Flow(SequentialTaskSet):
        def createVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.post(
                '/api/videos/',
                files={
                    'video': ('tester_video.mp4', open('files/tester_video.mp4', 'rb'), 'video/mp4')
                },
                headers=headers,
                name='/re-supply'
            )
            create_video.append(response.json()['video'])

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')
            
        @task
        def getAllVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                '/api/videos/',
                headers=headers
            )
            
            removed_video = random.choice(create_video)
            self.video_id = removed_video['_id']
            create_video.remove(removed_video)

        @task
        def deleteVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/videos/{self.video_id}',
                headers=headers,
                name='/deleted-videos'
            )

            self.createVideo()