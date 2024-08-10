from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Categories"


class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=0)
    rating = models.PositiveSmallIntegerField(choices=RatingChoices, default=RatingChoices.zero.value)
    discount = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.slug = None

    @property
    def discount_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'



class Comment(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name} => by comment'

    class Meta:
        db_table = 'Comments'


class Order(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=13)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Order"

    class Meta:
        db_table = 'order'
