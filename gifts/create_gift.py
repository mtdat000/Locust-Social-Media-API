from locust import HttpUser, task
from common.utils import salt, LOGIN_INFO

create_gift_id = []

class AdminBehaviour(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        while create_gift_id:
            id = create_gift_id.pop()
            self.client.delete(
                f'/api/gifts/{id}',
                headers=headers
            )
            print(len(create_gift_id))

    @task
    def createCategories(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.post(
            '/api/gifts/',
            {
                'name': 'Locust Test Category ' + salt(),
                'valuePerUnit': 69
            },
            files={
                'giftCreateImg': ('tester_img.jpg', open('files/tester_img.jpg', 'rb'), 'image/jpeg'),
            },
            headers=headers
        )
        create_gift_id.append(response.json()['gift']['_id'])