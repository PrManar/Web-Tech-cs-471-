from django.db import models

# Create your models here.


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # One address per student: use OneToOneField or ForeignKey with unique constraint.
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Address2(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}"

class Student2(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    addresses = models.ManyToManyField(Address2, blank=True, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField(default="2024-01-01T00:00:00Z")
    rating = models.SmallIntegerField(default=1)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title

class ItemImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='item_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
