from locust import HttpUser, task, between

class User(HttpUser):
    wait_time = between(1, 5)

    def onstart(self):
        response = self.client.post(
            url = "/api/auth/login", 
            json={
                'email': "admin@gmail.com", 
                'password': "Admin12345678#"
            }
        )
        self.accessToken = response.json().get('accessToken')
