from locust import HttpUser, TaskSet, task, constant
import random

class AdminBehaviour(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            {
                'email': "admin@gmail.com", 
                'password': "Admin12345678#"
            }
        )
        self.accessToken = response.json().get('accessToken')
    
    @task
    def createCategories(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        self.client.post(
            '/api/categories',
            {
                'name': 'Locust Test Category',
                'categoryUrl': ('tester_img.jpg', open('../files/tester_img.jpg', 'rb'), 'image/jpeg')
            },
            headers=headers
        )