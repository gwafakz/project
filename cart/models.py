from django.contrib.auth.models import User
from django.db import models

# Client Model (Stores Detailed Customer Info)
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Connects to Django's built-in User model
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)  # New field
    address = models.TextField(blank=True, null=True)  # New field
    city = models.CharField(max_length=100, blank=True, null=True)  # New field
    country = models.CharField(max_length=100, blank=True, null=True)  # New field
    zip_code = models.CharField(max_length=10, blank=True, null=True)  # New field

    def __str__(self):
        return self.name

# Order Model (Links to Client)
class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Links order to a client
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} by {self.client.name}"

# OrderItem Model (Stores Products in the Order)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Each order can have multiple items
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Order {self.order.id})"
