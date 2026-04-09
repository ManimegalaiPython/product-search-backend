from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    name        = models.CharField(max_length=200, db_index=True)
    description = models.TextField(db_index=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    rating      = models.FloatField(default=0.0)
    stock       = models.PositiveIntegerField(default=0)
    brand       = models.CharField(max_length=100, db_index=True)

    # ✅ ImageField — stores uploaded file in media/products/
    # Pillow must be installed: pip install Pillow
    image       = models.ImageField(upload_to='products/', null=True, blank=True)

    is_featured = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category', 'price']),
            models.Index(fields=['brand']),
        ]
