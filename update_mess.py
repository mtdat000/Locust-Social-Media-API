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


class AdminBehaviour(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/api/auth/login", 
            LOGIN_INFO['admin']
        )
        self.accessToken = response.json().get('accessToken')

    @task
    def updateMess(self):
        headers = {'Authorization': f'Bearer {self.accessToken}'}
        response = self.client.put(
            '/api/messages/674ec14350bfabd5921c8dd0',
            {
                'content': 'update mess ' + salt()
            },
            headers=headers
        )