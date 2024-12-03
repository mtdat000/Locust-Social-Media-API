from locust import HttpUser, SequentialTaskSet, task, between
from common.utils import LOGIN_INFO
import random

class UserBehavior(HttpUser):

    # Execute Task by the order that they are written using SequentialTaskSet
    @task
    class Flow(SequentialTaskSet):
        # Login as user
        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['bao']
            )
            self.accessToken = response.json().get('accessToken')

        # Get category list and pick a random category ID
        @task
        def getAllCategories(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/categories',
                headers=headers
            )

            # Pick a random category from list
            self.category_id = random.choice(response.json()['categories'])['_id']

        # Get category infomation with ID
        @task
        def getCategoryWithId(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            # Group multiple unique category by one name "/categories"
            self.client.get(
                f'/api/categories/{self.category_id}',
                headers=headers,
                name='/categories'
            )