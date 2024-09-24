from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.exceptions import ValidationError
from django.db import models


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='cooks_group',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='cooks_permission',
        blank=True,
    )

    class Meta:
        verbose_name = "Cook"
        verbose_name_plural = "Cooks"

    def clean(self):
        super().clean()
        if self.years_of_experience is not None and self.years_of_experience < 0:
            raise ValidationError("Years of experience must be greater than or equal to 0.")


class DishType(models.Model):
    name = models.CharField(max_length=100)

    def clean(self):
        super().clean()
        if not self.name:
            raise ValidationError("Name is required.")


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(Cook, related_name="dishes")

    def clean(self):
        super().clean()
        if self.price < 0:
            raise ValidationError("Price must be greater than or equal to 0.")
