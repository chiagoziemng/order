from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    date_sold = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.date_sold}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()

    def __str__(self):
        return f"Sale Item: {self.product.name} ({self.quantity_sold} units)"


class Invoice(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    invoice_number = models.CharField(max_length=10)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"


class ShoppingCartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
