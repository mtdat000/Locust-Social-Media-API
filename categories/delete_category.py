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

        for i in range(5):
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
        def createCategory(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}
            response = self.client.post(
                '/api/categories',
                {
                    'name': 'Locust Test Category ' + salt(),
                    'categoryUrl': ('tester_img.jpg', open('files/tester_img.jpg', 'rb'), 'image/jpeg')
                },
                name='/re-supply',
                headers=headers
            )
            create_category.append(response.json()['category'])

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
            removed_category = random.choice(create_category)
            self.category_id = removed_category['_id']
            create_category.remove(removed_category)

        @task
        def deleteCategoryWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                f'/api/categories/{self.category_id}',
                name='/deleted_categories',
                headers=headers
            )

            self.createCategory()