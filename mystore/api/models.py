from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.


class Products(models.Model):

    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    image = models.ImageField(null=True)

    def avg_rating(self):

        rattings = self.reviews_set.all().values_list('rating',flat=True)

        if rattings:

            return sum(rattings)/len(rattings)
        else:
            return 0

    def __str__(self):

        return self.name
    
class Carts(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    
class Reviews(models.Model):

    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comments = models.CharField(max_length=200)


    def __str__(self):

        return self.comments