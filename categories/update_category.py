from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO, salt
import random

create_category = []

class AdminBehaviour(HttpUser):
    def create_category(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        response = self.client.post(
            '/api/categories',
            {
                'name': 'Locust Test Category ' + salt(),
                'categoryUrl': ('tester_img.jpg', open('files/tester_img.jpg', 'rb'), 'image/jpeg')
            },
            headers=headers
        )
        create_category.append(response.json()['category'])

    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

        for i in range(10):
            self.create_category()

    def on_stop(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        while create_category:
            id = create_category.pop()['_id']
            self.client.delete(
                f'/api/categories/{id}',
                headers=headers
            )
            print(len(create_category))

    @task
    class Flow(SequentialTaskSet):
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def getAllCategories(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.get(
                '/api/categories',
                headers=headers
            )

            # Look up the list of category but only update categories that pre-created
            self.category_id = random.choice(create_category)['_id']

        @task
        def updateCategoryWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f'/api/categories/{self.category_id}',
                {
                    'name': 'Locust Test Updated Category ' + salt(),
                    'categoryUrl': ('tester_img.jpg', open('files/tester_img.jpg', 'rb'), 'image/jpeg')
                },
                name='/updated_categories',
                headers=headers
            )

        

        