from locust import HttpUser, task, SequentialTaskSet
from common.utils import LOGIN_INFO, salt
import random

class UserBehavior(HttpUser):
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
        def getAllExchangeRates(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/exchange-rate',
                headers=headers
            )

            exchangeRates = list(response.json()['exchangeRates'].keys())
            self.exchange_rate_name = random.choice(exchangeRates)

        @task
        def getExchangeRateByName(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            response = self.client.get(
                '/api/exchange-rate/by-name',
                params={
                    'name': self.exchange_rate_name
                },
                name='/exchange-rates-by-name',
                headers=headers
            )

            self.exchange_rate_id = response.json()['exchangeRate']['_id']

        @task
        def updateExchangeRateById(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.put(
                f'/api/exchange-rate/by-id/{self.exchange_rate_id}',
                json={
                    'value': round(random.uniform(0.01, 1), 5),
                    'description': 'Locust Test Exchange Rate ' + salt()
                },
                name='/updated-exchange-rates-by-id',
                headers=headers
            )