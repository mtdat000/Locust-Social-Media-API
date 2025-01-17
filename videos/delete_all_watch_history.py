from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_watch_history = []

class UserBehavior(HttpUser):
    def getRandomVideo(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.get(
            '/api/videos/',
            headers=headers
        )

        return random.choice(response.json()['videos'])['_id']

    def createWatchHistory(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.post(
            '/api/videos/user/watch-history',
            {
                'videoId': self.getRandomVideo()
            },
            headers=headers
        )
        create_watch_history.append(response.json()['historyRecord'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['bao']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(10):
            self.createWatchHistory()

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['bao']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        self.client.delete(
            f'/api/videos/user/watch-history',
            headers=headers
        )

        print('DONE')
        
    @task
    class Flow(SequentialTaskSet):        
        def getRandomVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/videos/',
                headers=headers
            )

            return random.choice(response.json()['videos'])['_id']
        
        def createWatchHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}
            
            response = self.client.post(
                '/api/videos/user/watch-history',
                {
                    'videoId': self.getRandomVideo()
                },
                headers=headers
            )
            create_watch_history.append(response.json()['historyRecord'])

        def createWatchHistoryList(self):
            for i in range(random.randint(2, 10)):
                self.createWatchHistory()

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')
            
        @task
        def deleteAllWatchHistory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/videos/user/watch-history',
                headers=headers
            )

            self.createWatchHistoryList()