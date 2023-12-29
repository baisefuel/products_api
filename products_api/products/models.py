from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to='products/', null=True, blank=True
    )
    Category = models.ForeignKey(
        Category, models.SET_NULL,
        related_name="products", blank=True, null=True
    )

    def __str__(self):
        return self.text[:30]


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
