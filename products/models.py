from django.db import models
from django.utils import timezone

from users.models import UserProfile


class Category(models.Model):
    id = models.AutoField(primary_key=True),
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True),
    title = models.CharField(max_length=200, blank=False, null=False)
    image = models.ImageField(upload_to='product/', default='product/default.png')
    content = models.TextField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    register_date = models.DateTimeField(default=timezone.now)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
