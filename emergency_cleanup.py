import requests
   
list = requests.get('https://manistreamapi.tuniapp.cc/api/gifts/').json()['gifts']

accessToken = requests.post(
    f"https://manistreamapi.tuniapp.cc/api/auth/login", 
    json={
      "email": "admin@gmail.com",
      "password": "Admin12345678#"
    }
    ).json()['accessToken']

headers={'Authorization': f'Bearer {accessToken}'},

for i in list:
    if('Locust Test Gift' in i['name']):
        id = i['_id']
        requests.delete(
            f'https://manistreamapi.tuniapp.cc/api/gifts/{id}',
            headers=headers
            )
        print('Delete', i['name'])