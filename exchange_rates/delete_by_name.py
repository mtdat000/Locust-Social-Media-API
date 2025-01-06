from locust import HttpUser, task, SequentialTaskSet
from common.utils import LOGIN_INFO, salt
import random

class UserBehavior(HttpUser):
    @task
    class Flow(SequentialTaskSet):
        def createExchangeRate(self, name):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            value = round(random.uniform(0.01, 1), 5)

            self.client.post(
                '/api/exchange-rate/',
                json={
                    'name': name,
                    'value': value,
                    'description': 'Locust Test Exchange Rate ' + salt()
                },
                headers=headers
            )

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
        def deleteExchangeRateByName(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            self.client.delete(
                '/api/exchange-rate/by-name',
                params={
                    'name': self.exchange_rate_name
                },
                name='/deleted-exchange-rates-by-name',
                headers=headers
            )

            self.createExchangeRate(self.exchange_rate_name)