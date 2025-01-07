from locust import HttpUser, task, SequentialTaskSet
from common.utils import salt, LOGIN_INFO
import random

create_exchange_rate_id = []
allow_name = [
      "topUpBalanceRate",
      "topUpCoinRate",
      "exchangeRateBalanceToCoin",
      "exchangeRateCoinToBalance",
      "coinPer1000View",
      "pointToCoin",
      "dailyPoint",
      "streakBonus",
      "ReceivePercentage",
    ]

class AdminBehaviour(HttpUser):
    # def on_stop(self):
    #     response = self.client.post(
    #         "/api/auth/login",
    #         LOGIN_INFO['admin']
    #     )
    #     accessToken = response.json().get('accessToken')

    #     headers = {'Authorization': f'Bearer {accessToken}'}

    #     while create_exchange_rate_id:
    #         id = create_exchange_rate_id.pop()
    #         self.client.delete(
    #             f'/api/exchange-rate/{id}',
    #             headers=headers
    #         )
    #         print(len(create_exchange_rate_id))

    @task
    class Flow(SequentialTaskSet):
        def clear(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            while create_exchange_rate_id:
                id = create_exchange_rate_id.pop()
                self.client.delete(
                    f'/api/exchange-rate/{id}',
                    headers=headers,
                    name='/cleanup'
                )

        @task
        def login(self):
            response = self.client.post(
                "/api/auth/login", 
                LOGIN_INFO['admin']
            )
            self.accessToken = response.json().get('accessToken')

        @task
        def createExchangeRate(self):
            headers = {'Authorization': f'Bearer {self.accessToken}'}

            value = round(random.uniform(0.01, 1), 5)

            response = self.client.post(
                '/api/exchange-rate/',
                json={
                    'name': random.choice(allow_name),
                    'value': value,
                    'description': 'Locust Test Exchange Rate ' + salt()
                },
                headers=headers
            )
            create_exchange_rate_id.append(response.json()['exchangeRate'][0]['_id'])

            # Don't use clear() method because some exchange rate might be used in other places
            #self.clear()