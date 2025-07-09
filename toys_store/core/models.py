from django.db import models
import uuid

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def create_client(self, name, email, dob):
        client = self.create(id = id, name = name, email = email, dob = dob)
        return client

class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sales')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'{self.client.name} - R${self.value} em {self.date}'
    
    def make_sale(self, client, value, date):
        sale = self.create(client = client, value = value, date = date)
        return sale