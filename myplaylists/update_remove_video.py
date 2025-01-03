from locust import HttpUser, TaskSet, SequentialTaskSet, task
from common.utils import salt, LOGIN_INFO
import random

create_playlist = []

class UserBehavior(HttpUser):
    def getRandomVideo(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.get(
            '/api/videos/',
            params={
                'enumMode': 'public'
            },
            headers=headers,
            name='/get-random-video'
        )
        
        return random.choice(response.json()['videos'])

    def updateAddVideo(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        video_list = self.client.get(
                f'/api/my-playlists/{self.playlist_id}',
                headers=headers,
                name='/access-playlist'
            ).json()['playlist']['videoIds']

        video_id = self.getRandomVideo()['_id']

        while video_id in video_list:
            video_id = self.getRandomVideo()['_id']

        self.client.put(
            f'/api/my-playlists/{self.playlist_id}/add-video',
            {
                'videoId': video_id,
            },
            headers=headers,
            name='/video-added'
        )

    def createVideo(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        locust_identifier = 'Locust Test Playlist ' + salt()

        response = self.client.post(
            '/api/my-playlists',
            {
                'playlistName': locust_identifier,
                'description': locust_identifier,
                'enumMode': 'public',
                'playlistCreate': None,
            },
            headers=headers
        )
        playlist = response.json()['playlist']
        self.playlist_id = playlist['_id']

        create_playlist.append(playlist)
        for i in range(random.randint(1, 3)):
            self.updateAddVideo()

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['bao']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(3):
            self.createVideo()

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['bao']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_playlist:
            id = create_playlist.pop()['_id']
            self.client.delete(
                f'/api/my-playlists/{id}',
                headers=headers,
                name='/cleanup'
            )
            print(len(create_playlist))

    @task
    class Flow(SequentialTaskSet):
        def getRandomPlaylistVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                f'/api/my-playlists/{self.playlist_id}',
                headers=headers,
                name='/access-playlist'
            )

            if(len(response.json()['playlist']['videoIds']) == 0):
                return None

            return random.choice(response.json()['playlist']['videoIds'])
        
        def getRandomVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/videos/',
                params={
                    'enumMode': 'public'
                },
                headers=headers,
                name='/get-random-video'
            )
            
            return random.choice(response.json()['videos'])
        
        def updateAddVideo(self, video_id):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f'/api/my-playlists/{self.playlist_id}/add-video',
                {
                    'videoId': video_id,
                },
                headers=headers,
                name='/video-added'
            )

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')
            self.userId = response.json().get('userId')
            
        @task
        def getAllUserPlaylist(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                f'/api/my-playlists/user/{self.userId}',
                headers=headers,
                name='/user-playlists'
            )

            self.playlist_id = random.choice(create_playlist)['_id']

        @task
        def updateRemoveVideo(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            remove_video_id = self.getRandomPlaylistVideo()
            
            if(remove_video_id != None):
                self.client.put(
                    f'/api/my-playlists/{self.playlist_id}/remove-video',
                    {
                        'videoId': remove_video_id,
                    },
                    headers=headers,
                    name='/video-removed'
                )

                self.updateAddVideo(remove_video_id)

            else:
                self.updateAddVideo(self.getRandomVideo()['_id'])