from locust import HttpUser, TaskSet, task, constant
import random
import string

LOGIN_INFO = {
    'admin': {
      "email": "admin@gmail.com",
      "password": "Admin12345678#"
    },
    'bao': {
      "email": "n.bao25702@gmail.com",
      "password": "P@ssword1"
    },
    'khang': {
      "email": "khangtuhuu@gmail.com",
      "password": "Aa123456789!"
    }
}

def salt(size=15, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

create_category_id = []

class AdminBehaviour(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

    def on_stop(self):
        response = self.client.post(
            "/api/auth/login",
            LOGIN_INFO['admin']
        )
        accessToken = response.json().get('accessToken')
        headers = {'Authorization': f'Bearer {accessToken}'}

        while create_category_id:
            id = create_category_id.pop()
            self.client.delete(
                f'/api/categories/{id}',
                headers=headers
            )
            print('Delete', id)

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