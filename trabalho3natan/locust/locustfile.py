#POST1MB
#https://expertturismo.com/wp-content/uploads/2023/10/Agencia-de-viagem-natalrn-370-%C3%97-270-px-1-1.png
#http://localhost/?p=18

#POST400KB
#https://laviaitalia.com.br/wp-content/uploads/2025/03/hub-primavera-3200x1800-1.webp
#http://localhost/?p=15

#Texto 400KB
#http://localhost/?p=13

"""
Teste de carga WordPress - 3 páginas:
 • /?p=18  (imagem 1 MB)
 • /?p=15  (imagem 400 KB)
 • /?p=13  (texto 400 KB)
"""

import os
from locust import HttpUser, task, between

class WordPressUser(HttpUser):
    host = os.getenv("ATTACKED_HOST", "http://localhost")
    wait_time = between(1, 3)

    @task(1)
    def post_img_1mb(self):
        self.client.get("/?p=18", name="POST 1 MB")

    @task(1)
    def post_img_400kb(self):
        self.client.get("/?p=15", name="POST 400 KB (img)")

    @task(1)
    def post_text_400kb(self):
        self.client.get("/?p=13", name="POST 400 KB (texto)")



