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
                headers=headers
            )
            print(len(create_video))
        
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
        def getAllVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                '/api/videos/',
                headers=headers
            )

            self.video_id = random.choice(create_video)['_id']

        @task
        def updateVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            locust_identifier = 'Locust Update Test Video ' + salt()

            self.client.patch(
                f'/api/videos/{self.video_id}',
                {
                    'title': locust_identifier,
                    'description': locust_identifier,
                    'categoryIds': [
                        '673422fc818ae4a0ad74b229'
                    ],
                    'enumMode': 'public',
                    'videoThumbnail': None
                },
                headers=headers,
                name='/updated-videos'
            )