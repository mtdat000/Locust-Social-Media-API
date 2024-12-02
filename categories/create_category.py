from locust import HttpUser, TaskSet, task, constant
import random
import string

create_category_id = []

def salt(size=15, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login", 
            {
                'email': "admin@gmail.com", 
                'password': "Admin12345678#"
            }
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        for i in create_category_id:
            self.client.delete(
                f'/api/categories/{i}',
                headers=headers
            )
            print('Delete', i)
    
    @task
    def createCategories(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}

        response = self.client.post(
            '/api/categories',
            {
                'name': 'Locust Test Category ' + salt(),
                'categoryUrl': ('tester_img.jpg', open('../files/tester_img.jpg', 'rb'), 'image/jpeg')
            },
            headers=headers
        )
        create_category_id.append(response.json()['category']['_id'])