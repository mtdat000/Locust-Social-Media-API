from locust import HttpUser, TaskSet, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO

create_playlist_id = []

class AdminBehaviour(HttpUser):
    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_playlist_id:
            id = create_playlist_id.pop()
            self.client.delete(
                f'/api/my-playlists/{id}',
                headers=headers
            )
            print(len(create_playlist_id))

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
        def createPlaylist(self):
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
            create_playlist_id.append(response.json()['playlist']['_id'])