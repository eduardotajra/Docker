from locust import HttpUser, task, between
import yaml, random

# Carrega o mapeamento dos cenários
with open("/mnt/locust/posts.yaml") as f:
    POSTS = yaml.safe_load(f)

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def read_post(self):
        slug, meta = random.choice(list(POSTS.items()))
        with self.client.get(f"/?p={meta['id']}", name=meta['label'], catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Erro {resp.status_code}")
