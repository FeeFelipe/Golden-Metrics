from locust import HttpUser, task, between
import os

class OrdersUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(5)
    def get_orders(self):
        self.client.get("/orders")

    @task(1)
    def health(self):
        self.client.get("/health")
