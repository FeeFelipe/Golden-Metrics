from locust import HttpUser, task, between
import random

class OrderUser(HttpUser):
    wait_time = between(0.1, 1)

    @task
    def get_orders(self):
        self.client.get("/orders")

    @task
    def get_health(self):
        self.client.get("/health")
