from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    def on_start(self):
        response = self.client.post("/api/auth/login", json={"email": "admin@gmail.com", "password": "Admin12345678#"})
        self.token = response.json()["accessToken"]
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

    @task(1)
    def create_stream(self):
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

        # Lấy danh sách category
        response_categories = self.client.get("/api/categories", headers=headers)
        if response_categories.status_code == 200:
            categories = response_categories.json().get("categories", [])
            if categories:
                # Chọn ngẫu nhiên một category
                selected_category = random.choice(categories)
                category_id = selected_category["_id"]

                # Dữ liệu tạo mới stream
                stream_data = {
                    "title": "test tiz",
                    "description": "string",
                    "categoryIds": [category_id]
                }

                # Tạo mới stream
                response_create = self.client.post("/api/streams", json=stream_data, headers=headers)
                if response_create.status_code == 201:
                    print(f"Successfully created stream with title {stream_data['title']}")
                else:
                    print(f"Failed to create stream: {response_create.status_code}")
            else:
                print("No categories found")
        else:
            print(f"Failed to get categories: {response_categories.status_code}")